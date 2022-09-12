'''Twitter Posts. Analyser by Alexander Krasnov

It takes one or more tab-delimited (TSV) data file(s) containing tweets
scrapped with "tw_scrapper.py", concats them all together into the single
data frame, and then performs data analysis. To make bot analysis the
"bots.txt" file should be present in the same folder and contain the list
of Twitter bots.

The result of analysis is placed into the JS-variable in "charts_data.js" file
'''


import sys, json
import pandas as pd, numpy as np

from collections import Counter


#
#   Input files
#

fn_in = sys.argv[1:] or \
        input('Enter one or more file names delimited by space containing tab-separated (TSV) data:').split()


#
#   Making single data frame
#

print('==> Reading TSV-file(s)')

df = pd.DataFrame()

for fn in fn_in:
    print('\t', fn)

    df = pd.concat([
        df, pd.read_csv(fn, delimiter='\t', dtype=str)
    ])

df = df.drop_duplicates('id_str', keep='last').reindex()


#
#   Data type conversion and limitation
#

print('==> Parsing dates')

# Parsing and converting to native datetime64 data type
df.created_at = pd.to_datetime(df.created_at)

# Uncomment and change datetime to limit data
#df = df[(df.created_at >= '2021-01-04 16:00') & (df.created_at < '2021-01-06 00:00')]

print('==> Converting data types and filling NaNs')

# Converting geo coords to boolen value, i.e. geo coords is present or not
# Possible input values: 0/1, or NaN/Location
# Output values: 0/NaN -> False, 1/String -> True
df.geo_coordinates = (df.geo_coordinates.fillna('0') != '0')

# Filling NaNs with zero values and converting them to int64 data type
fields = [
    'id_str',
    'in_reply_to_user_id_str',
    'from_user_id_str',
    'in_reply_to_status_id_str',
    'user_followers_count',
    'user_friends_count',
    #'geo_coordinates'
]

df[fields] = df[fields].fillna(0).astype(np.int64)


#
#   Analysis
#

print('==> Analysing data')

# Retweets only including bots
retweets_bots = (df.text.str[:2] == 'RT')

# Top retweeters and tweeters including bots
top_rt_bots = df[ retweets_bots].from_user.value_counts().sort_values(ascending=False)
top_tw_bots = df[~retweets_bots].from_user.value_counts().sort_values(ascending=False)

# Filtering bots using predefined list of bots in the "bots.txt" file
try:
    with open('bots.txt', 'r', encoding='utf-8') as f:
        bots = '|'.join(
            list(
                filter(
                    lambda b: b != '',
                    f.read().split(sep='\n')
                )
            )
        )

        df_bots_size = df.id_str.size

        # Removing bots if list of bots is loaded
        if bots:
            df = df[~df.from_user.str.contains(bots, case=False, regex=True)]

        df_bots_num = df_bots_size - df.id_str.size

except FileNotFoundError:
    print('==> The file "bots.txt" is not found.\n')

# Retweets without bots
retweets = df.text.str[:2] == 'RT'

# Top retweeters and tweeters without bots
top_rt = df[ retweets].from_user.value_counts().sort_values(ascending=False)
top_tw = df[~retweets].from_user.value_counts().sort_values(ascending=False)

# Top 10 retweeters and tweeters
top_rt_10 = top_rt[:10]
top_tw_10 = top_tw[:10]

# % of retweets/tweets which came from the top 10 retweeters/tweeters
pct_top_rt_10 = np.round(np.sum(top_rt_10) * 100 / np.sum( retweets), 1)
pct_top_tw_10 = np.round(np.sum(top_tw_10) * 100 / np.sum(~retweets), 1)

# Who tweeted from top 10 retweeters and vice versa
top_rt_tw = df.from_user[~retweets & df.from_user.isin(top_rt_10.index)].value_counts().sort_values(ascending=False)
top_tw_rt = df.from_user[ retweets & df.from_user.isin(top_tw_10.index)].value_counts().sort_values(ascending=False)

# Who was the bot in top tweeters/retweeters lists
bots_rt = top_rt_bots[top_rt_bots.index.symmetric_difference(top_rt.index)].dropna().sort_values(ascending=False)[:20]
bots_tw = top_tw_bots[top_tw_bots.index.symmetric_difference(top_tw.index)].dropna().sort_values(ascending=False)[:20]

# Retweets and tweets amount and percentage
cnt_rt = np.sum( retweets)
cnt_tw = np.sum(~retweets)

# Unique users and their posting rate
unique_users = df.from_user.unique().size
unique_users_rate = np.round(df.id_str.size / unique_users, 1)

# Unique retweeters and their posting rate
unique_users_rt = df[retweets].from_user.unique().size
unique_users_rt_rate = np.round(df[retweets].id_str.size / unique_users_rt, 1)

# Unique tweeters and their posting rate
unique_users_tw = df[~retweets].from_user.unique().size
unique_users_tw_rate = np.round(df[~retweets].id_str.size / unique_users_tw, 1)

# Top five retweets
top_retweets = df[retweets].text.value_counts().sort_values(ascending=False)[:10]

# % are geocoded
geo_total = np.sum(df.geo_coordinates)
#geo_coded = np.round(geo_total * 100 / df.id_str.size, 3)

# % of profiles have a location
have_location_total = df[~df.user_location.isna()].from_user.unique().size

# Top 10 followers
top_followers = df.sort_values(by=['user_followers_count', 'user_friends_count'], ascending=False).drop_duplicates('from_user_id_str', keep='first')[['from_user', 'user_followers_count', 'user_friends_count']][:10]

# Hashtags and mentions
hashtags = Counter()
mentions = Counter()

for ent in df.entities_str:
    try:
        e = json.loads(ent)

        if e['hashtags']:
            for h in e['hashtags']:
                #hashtags.update(['#' + h['text']])
                hashtags.update(['#' + h['text'].lower()])

        if e['user_mentions']:
            for m in e['user_mentions']:
                mentions.update(['@' + m['screen_name']])

    except TypeError:
        print(ent)

cnt_hashtags = sum(hashtags.values())
cnt_mentions = sum(mentions.values())

hashtags = dict(hashtags.most_common(10))
mentions = dict(mentions.most_common(10))

hashtags.update({'Others': cnt_hashtags - sum(hashtags.values())})
mentions.update({'Others': cnt_mentions - sum(mentions.values())})

# Timeseries for all posts
ts = df.set_index(pd.DatetimeIndex(df.created_at)).sort_index(ascending=True)['id_str']

# Making 10min timeseries resample
ts_10min = ts.resample('10min').count()

# 10min timeseries for retweets
df_ts_rt = df[retweets][['created_at', 'id_str']]
ts_rt = df_ts_rt.set_index(pd.DatetimeIndex(df_ts_rt.created_at)).sort_index(ascending=True)['id_str']

ts_rt_10min = ts_rt.resample('10min').count()

del(df_ts_rt)

# 10min timeseries for tweets
df_ts_tw = df[~retweets][['created_at', 'id_str']]
ts_tw = df_ts_tw.set_index(pd.DatetimeIndex(df_ts_tw.created_at)).sort_index(ascending=True)['id_str']

ts_tw_10min = ts_tw.resample('10min').count()

del(df_ts_tw)

# Calculating users tweeting and retweeting this many times
vol_rt = dict()
vol_tw = dict()

for i in range(1, 10):
    vol_tw[str(i)] = int(np.sum(top_tw == i))
    vol_rt[str(i)] = int(np.sum(top_rt == i))

vol_tw['10+'] = int(np.sum(top_tw >= 10))
vol_rt['10+'] = int(np.sum(top_rt >= 10))

#
#   Generating data file for charts.js plotting script
#

print('==> Saving to the file')

res = {
    'cnt_rt': int(cnt_rt),
    'cnt_tw': int(cnt_tw),
    'records_total': int(df.id_str.size),
    'records_removed': int(df_bots_num),
    # Timeseries for both tweets and retweets
    'ts1_chart': {
        'dtm': ts_10min.index.strftime('%Y-%m-%d %H:%M').tolist(),
        'val': ts_10min.values.tolist()
    },
    # Timeseries for retweets and tweets
    'ts2_chart': {
        'dtm': ts_rt_10min.index.strftime('%Y-%m-%d %H:%M').tolist(),
        'val_rt': ts_rt_10min.values.tolist(),
        'val_tw': ts_tw_10min.values.tolist()
    },
    # top retweeter including bots
    'top_rt_bots': {
        'users': ('@' + top_rt_bots[:10].index).tolist(),
        'tweets': top_rt_bots[:10].values.tolist()
    },
    # top tweeter including bots
    'top_tw_bots': {
        'users': ('@' + top_tw_bots[:10].index).tolist(),
        'tweets': top_tw_bots[:10].values.tolist()
    },
    # These users are bots from the list of top retweeters
    'top_rt_bot_list': ('@' + bots_rt.index).tolist(),
    # These users are bots from the list of top tweeters
    'top_tw_bot_list': ('@' + bots_tw.index).tolist(),
    # top 10 retweeters without bots (retweets)
    'top_10_rt': {
        'users': ('@' + top_rt_10.index).tolist(),
        'tweets': top_rt_10.values.tolist()
    },
    # top 10 tweeters without bots (tweets)
    'top_10_tw': {
        'users': ('@' + top_tw_10.index).tolist(),
        'tweets': top_tw_10.values.tolist()
    },
    # % of retweets/tweets which came from the top 10 retweeters/tweeters
    #'pct_top_rt_10': pct_top_rt_10,
    #'pct_top_tw_10': pct_top_tw_10,
    # top 10 retweeters without bots (tweets)
    'top_10_rt_tw': {
        'users': ('@' + top_rt_tw.index).tolist(),
        'tweets': top_rt_tw.values.tolist()
    },
    # top 10 tweeters without bots (retweets)
    'top_10_tw_rt': {
        'users': ('@' + top_tw_rt.index).tolist(),
        'tweets': top_tw_rt.values.tolist()
    },
    # Unique users and rates
    'unique_users': int(unique_users),
    'unique_users_rate': unique_users_rate,
    'unique_users_rt': int(unique_users_rt),
    'unique_users_rt_rate': unique_users_rt_rate,
    'unique_users_tw': int(unique_users_tw),
    'unique_users_tw_rate': unique_users_tw_rate,
    # Top 10 tweets
    'top_retweets': {
        'text': top_retweets.index.tolist(),
        'count': top_retweets.values.tolist()
    },
    'geo_coded': {
        'enabled': int(geo_total),
        'disabled': int(df.id_str.size - geo_total)
    },
    'have_location': {
        'yes': int(have_location_total),
        'no': int(unique_users - have_location_total)
    },
    'top_10_popular': {
        'users': ('@' + top_followers.from_user).tolist(),
        'followers': top_followers.user_followers_count.tolist(),
        'friends': top_followers.user_friends_count.tolist(),
    },
    'hashtags': {
        'tags': list(hashtags.keys()),
        'count': list(hashtags.values()),
        'percent': list(np.round(np.fromiter(hashtags.values(), dtype=int) * 100 / cnt_hashtags, 1))
    },
    'mentions': {
        'users': list(mentions.keys()),
        'count': list(mentions.values()),
        'percent': list(np.round(np.fromiter(mentions.values(), dtype=int) * 100 / cnt_mentions, 1))
    },
    'volumes': {
        'number': list(vol_tw.keys()),
        'tweeters': list(vol_tw.values()),
        'retweeters': list(vol_rt.values())
    }
}

#
#   Saving the result of analysis into "charts_data.js"
#

fn_out = 'charts_data.js'

with open(fn_out, 'w', newline='', encoding='utf-8') as f:
    f.write('var ch_data = ')
    f.write(json.dumps(res, indent=4, ensure_ascii=False))


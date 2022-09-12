'''Twitter Posts. Scrapper by Alexander Krasnov

Collects tweets by a given search string and saves the output data
in the tab-delimited (TSV) file.

Optional boolean parameter "dump_json" performs data saving in JSON
file format for each tweet in.
'''


import tweepy, json, csv, sys

from datetime import date, timedelta, datetime
from time import sleep


OAUTH_TOKEN = '<your_oauth_token>'
OAUTH_TOKEN_SECRET = '<your_oauth_token_secret>'
CONSUMER_KEY = '<your_consumer_key>'
CONSUMER_SECRET = '<your_consumer_secret>'


def clean(s):
    trims = ('\n', '\r', '\t')

    if s:
        for t in trims:
            s = s.replace(t, ' ')

    return s


def nan2num(i):
    return int(i) if i else 0


def tw_status(tweet):
    try:
        return [
            tweet['id_str'],
            clean(tweet['user']['screen_name']),
            clean(tweet['full_text'] if 'full_text' in tweet else tweet['text']),
            tweet['created_at'],
            int(tweet['user']['geo_enabled']),
            tweet['lang'],
            nan2num(tweet['in_reply_to_user_id_str']),
            clean(tweet['in_reply_to_screen_name']),
            tweet['user']['id_str'],
            nan2num(tweet['in_reply_to_status_id_str']),
            tweet['source'],
            tweet['user']['profile_image_url'],
            tweet['user']['followers_count'],
            tweet['user']['friends_count'],
            clean(tweet['user']['location']),
            tweet['user']['url'],
            json.dumps(tweet['entities'])
        ]
    except KeyError as e:
        with open('error.log', 'a', newline='\n', encoding='utf-8') as err:
            err.write('{},{}:\n{}\n'.format(
                sys.argv[0],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                json.dumps(tweet, indent=4)
            ))
            err.write('Exception KeyError: ' + str(e) + '\n')
            err.write('-'*50 + '\n')

        return []

    except:
        print('Exception!', json.dumps(tweet, indent=4))

        return []


def tw_scrap(query_str, output_fn, dump_json=False):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    twitter_api = tweepy.API(
            auth,
            wait_on_rate_limit=True,
        )

    with open(output_fn, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t', quotechar = '"', quoting=csv.QUOTE_MINIMAL)

        csvwriter.writerow(['id_str', 'from_user', 'text', 'created_at', 'geo_coordinates', 'user_lang', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'from_user_id_str', 'in_reply_to_status_id_str', 'source', 'profile_image_url', 'user_followers_count', 'user_friends_count', 'user_location', 'status_url', 'entities_str'])

        i = 1

        today = date.today()

        #start_date = date(2022, 2, 24)
        until_date = date(2022, 2, 23)

        #max_id = ...
        #since_id = max_id - 100000

        try:
            tweets = tweepy.Cursor(
                twitter_api.search_tweets,
                q=query_str,
                lang='en',
                #result_type='mixed', #'recent' or 'popular'
                #max_id=str(max_id),
                #since_id=str(since_id),
                #since=start_date,
                #until=until_date,
                until='2022-06-23',
                tweet_mode='extended'
            #).items(200000)
            ).items()

            for tweet in tweets:
                if dump_json:
                    with open('tweets/' + tweet.id_str + '.json', 'w', encoding='utf-8') as f:
                        f.write(
                            json.dumps(tweet._json, indent=4, ensure_ascii=False)
                        )

                tw = tw_status(tweet._json)

                if 'retweeted_status' in tweet._json:
                    st = tw_status(tweet._json['retweeted_status'])

                    tw[2] = 'RT @' + st[1] + ': ' + st[2]
                    tw[15] = st[15]

                    #if 'quoted_status' in tweet._json:
                    #    st = tw_status(tweet._json['quoted_status'])

                    #    tw[2] = tw[2] + ' ' + st[15]

                #elif 'quoted_status' in tweet._json:
                #    st = tw_status(tweet._json['quoted_status'])

                #    tw[2] = tw[2] + ' ' + st[15]

                csvwriter.writerow(tw)

                print(i, tw[3])

                i = i + 1

                # Time limit bypass when the scrapping process expects fatal issue
                # Normally, Tweepy module should handle it automatically
                # Sleep for 150 seconds every 450 tweets
                #if i > 450:
                #    print('Sleep for 150 sec to bypass Twitter API rate limit')

                #    sleep(150)

                #    i = 1

        except tweepy.TweepyException as e:
            print(e)


if __name__ == '__main__':

    try:
        query_str = sys.argv[1]
    except IndexError:
        query_str = input('Enter search string:')

    try:
        output_fn = sys.argv[2] if sys.argv[2][-4:] == '.csv' else sys.argv[2] + '.csv'
    except IndexError:
        output_fn = input('Enter output csv filename:')


    #tw_scrap(query_str, output_fn, dump_json=True)
    tw_scrap(query_str, output_fn)

'''Twitter Posts. Wordcloud builder by Alexander Krasnov

It takes one or more tab-delimited (TSV) data file(s) containing tweets scrapped
with "tw_scrapper.py", and tokenizes data from the single column named "text" into
the single list of tokens, and then performs wordcloud analysis.

The wordcloud data is placed both into the JS-variable in "charts_data.js" file,
and tab-delimited (TSV) data file. The TSV data is more convinient for using with
online wordcloud services like wordart.com, worditout.com, etc.
'''


import sys, csv, re, math, json

from collections import Counter

from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize


def clean(text):
    procs = [
        ('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', ' '),
        ('[“”]', '"'),
        ('[’‘`]', "'"),
        ('@\w+|&amp;', ' '),
        ('[^\x00-\x7F]+', ''), # strips non-ascii characters
        #('[^a-zA-Z\d]', ''), # strips non-latin characters
        #('[\~\–\-\!\?\|\#\$\%\^\&\\\:\;]', ' '),
    ]

    text = text.replace('RT @', '@')

    for p, r in procs:
        text = re.sub(p, r, text)

    return text


if __name__ == '__main__':
    fn_in = sys.argv[1:] or \
            input('Enter one or more file names delimited by space containing tab-separated (TSV) data:').split()

    # Reading only the text content of the Twitter's posts stored in TSV-file

    #w_chr = '\\|/—'
    w_chr = '┐┤┘┴└├┌┬'

    text_tokens = []

    print('==> Reading TSV-file and tokenizing text')

    for fn in fn_in:
        with open(fn, 'r', encoding='utf-8') as f:
            csvreader = csv.DictReader(f, dialect='excel-tab')

            w = 0

            cnt_prev = -1

            for text in map(lambda x: clean(x['text']).lower(), csvreader):
                cnt_done = len(text_tokens) // 10000
                text_tokens += word_tokenize(text)

                if cnt_done != cnt_prev:
                    cnt_prev = cnt_done

                    print('\t' + fn + '\t' + w_chr[w], end='\r')

                    #w = (0 if w == len(w_chr)-1 else w+1)
                    if w == len(w_chr) - 1:
                        w = 0
                    else:
                        w = w + 1

            print('\t' + fn + '\t --> Done')

    # Counting words

    c = len(text_tokens)
    words_count = Counter()

    i = 1
    pct_prev = -1

    print('==> Counting words')

    for word in text_tokens:
        pct_done = int(i / c * 100)

        if pct_prev != pct_done:
            print(f'\t{pct_done}%', end='\r')

            pct_prev = pct_done

        if len(word) > 3 and not word.isnumeric() and word not in stopwords.words('english') and wordnet.synsets(word, lang='eng'):
            words_count.update([wordnet.morphy(word)])

        i += 1

    print()

    # Writing wordcloud data to the TSV-file

    norm_func = lambda x: x   # no scaling
    #norm_func = math.log      # logarithm scale
    #norm_func = math.sqrt     # square root scale
    
    with open('wordcloud.txt', 'w', newline='', encoding='utf-8') as csvfile:
        print('==> Writing to the TSV-file\n')

        csvwriter = csv.writer(csvfile, delimiter='\t', quotechar = '"', quoting=csv.QUOTE_MINIMAL)

        # Uncomment the line below if the header is required in the output file
        #csvwriter.writerow(['Word', 'Count'])

        # First 1000 words
        for i, v in words_count.most_common(1000):
            csvwriter.writerow([i, norm_func(v)])


    # Statistics

    print('Unique words:', len(words_count))
    print('Total words:', sum(words_count.values()))


    # Writing into JS-file top-200 words

    wc_data = []

    for w, c in words_count.most_common(200):
        wc_data.append({
            'text': w,
            'count': c
        })

    with open('wordcloud_data.js', 'w', newline='', encoding='utf-8') as jsfile:
        jsfile.write('var wc_data = ')
        jsfile.write(json.dumps(wc_data, ensure_ascii=False) + ';')


    # First 30 words just for information

    print('\n', words_count.most_common(30))
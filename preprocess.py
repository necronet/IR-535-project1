import os
import json
import re
import time
import emoji

''' Take the field of a full tweet and output a new compacted tweet with only the
    required fields. As describe in the hw the fields are as follow:

    - city
    - tweet_lang
    - tweet_loc
    - tweet_text
    - topic
    - hashtags
    - user_mentions
    - tweet_xx
    - tweet_date
'''

def extract_emojis(str):
  return ''.join(c for c in str if c in emoji.UNICODE_EMOJI)

def compact_tweet(tweet,city,topic):

    if topic =='social_unrest' :
        topic = 'social unrest'
    if topic == 'infrastructure':
        topic = 'infra'
    hashtags = re.findall(r"#(\w+)", tweet['text'])
    hashtags_text = None
    hashtags_text = ', '.join(hashtags).strip()

    mentions = re.findall(r"@(\w+)", tweet['text'])
    mentions_text = None
    mentions_text = ', '.join(mentions).strip()

    emoji_pattern = re.compile(u'['
                        u'\U0001F300-\U0001F5FF'
                        u'\U0001F600-\U0001F64F'
                        u'\U0001F680-\U0001F6FF'
                        u'\u2600-\u26FF\u2700-\u27BF]+',
                        re.UNICODE)

    emojis = extract_emojis(tweet['text'])
    rtext = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(rtext,tweet['text'])
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

    #text = emoji_pattern.sub(r'', tweet['text'])
    #print(tweet['text'])
    #print(text)

    coords = None
    if tweet["geo"]:
        coords = tweet["geo"]['coordinates']

    #print(city.lower())

    return {
            "city":city.lower(), "tweet_lang":tweet['lang'],"topic":topic,
            "text":tweet['text'],
            'hashtags':hashtags_text,
            'tweet_urls':urls,
            'mentions':mentions_text,
            "tweet_date":ts,
            "tweet_loc": coords,
            'tweet_emoticons':emojis
            }
            # ,
            #

def open_twitter_json(file):
    file_name = os.path.basename(os.path.normpath(file))
    results = json.load(open(file))
    return results

def list_twitter_files(basedir = './results/'):
    files = []
    objects = os.listdir(basedir)
    for file in objects:
        if file.endswith('.json'):
            files.append(basedir+'/'+file)
    return files

if __name__ == '__main__':
    print("Preprocessing the data")
    topics = ['environment','crime','infrastructure','politics','social_unrest']
    for topic in topics:
        twitter_files = list_twitter_files('./results/{}'.format(topic))
        tweets = []
        #print('files in {} are {}'.format(topic,len(twitter_files)))
        for twitter_file in twitter_files:
            for city in ["NYC","Delhi","Bangkok","Paris","Mexico City"]:
                if city in twitter_file: break
                else:
                     city = None

            if city not in twitter_file:
                print(twitter_file)
                continue

            twitter_json = open_twitter_json(twitter_file)
            for tweet in twitter_json:
                if tweet['lang'] in ['es','en','fr','hi','th']:
                    tweets.append(compact_tweet(tweet,city,topic))

        print('Saving {} preprocessed data for {}'.format(len(tweets),topic))

        with open("./processed/{}.json".format(topic), 'w', encoding='utf8') as fp:
            json.dump(tweets, fp)

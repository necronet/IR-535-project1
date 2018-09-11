import os
import json

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
def compact_tweet(tweet,city,topic):
    return {
            "city":city, "tweet_lang":tweet['lang'],"topic":topic,
            "tweet_text":tweet['text'],
            "tweet_{}".format(tweet['lang']):tweet['text'],
            "tweet_date":tweet['created_at'],
            "hashtags":tweet['entities']['hashtags'],
            "user_mentions":tweet['entities']['user_mentions'],
            "tweet_loc": tweet["geo"]
            }

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
        for twitter_file in twitter_files:
            for city in ["NYC","Delhi","Bangkok","Paris","Mexico City"]:
                if city in twitter_file: break

            twitter_json = open_twitter_json(twitter_file)
            for tweet in twitter_json:
                tweets.append(compact_tweet(tweet,city,topic))

        print('Saving {} preprocessed data for {}'.format(len(tweets),topic))
        with open("./processed/{}.json".format(topic), 'w', encoding='utf8') as fp:
            json.dump(tweets, fp)

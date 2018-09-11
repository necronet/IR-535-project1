import tweepy
import itertools
import datetime
import random
import json
from tweepy.error import TweepError
from config import get_twitter_config
from tweepy import OAuthHandler, API, Cursor, Stream

config = get_twitter_config()

def start_crawl(api):
    dates = get_dates()
    languages = get_languages()

    for key in get_topic().keys():
        topics = get_topic()[key]
        cities = get_cities()
        search_terms = itertools.product(topics, cities)
        for search_term in search_terms:
            for day in dates:
                for lang in languages:
                    term = ' '.join(search_term)
                    filename = 'results/{}/{}-{}-{}.json'.format(key,term,lang,day)
                    try:
                        results = tweepy.Cursor(api.search, q=term,
                                    lang=lang,show_user=True,
                                    include_entities=True,count=100,
                                    until=day).pages()
                        for result in results:
                            print("Searched: {} count:{} lang:{}".format(term, len(result),lang))
                            searched_tweets = [status._json for status in result]
                            with open(filename, 'w', encoding='utf8') as fp:
                                json.dump(searched_tweets, fp)

                    except TweepError as err:
                        print("Error occured for {} on {} - message: [{}]".format(term,day,err))
                        #logging.info("Error occured for {} on {} - message: [{}]".format(query,date,err))


def get_dates(days=5):
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, days)]
    formatted_dates = [date_.strftime('%Y-%m-%d') for date_ in date_list]
    random.shuffle(formatted_dates)
    return formatted_dates

def get_languages():
    return ["hi","th","fr","es","en"]

def get_cities():
    return ["NYC","Delhi","Bangkok","Paris","Mexico City"]

def get_topic():
    return {"crime":
            ["robbery","murder","assesination","mug","thugs","gangs crime","arrest","burglar"],
            "environment":
            ["hurricane","smog","pollution","air quality","food","droughts","dust","storm"],
            "politics":
            ["senator","politics","governor","democrats","republicans","Trump","US politics"],
            "social_unrest":
            ["Strikes","protest","riots","police riots","uprising"],
            "infrastructure":
            ['roads','electrical power','water','sanitation','airport infrastructure','bridge','Dam',
            'water supply','sewers','electrical grids','telecommunications']}


if __name__ == '__main__':
    auth = OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    start_crawl(api)

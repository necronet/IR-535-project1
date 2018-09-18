import tweepy
import itertools
import datetime
import random
import json
import uuid
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
        search_terms = itertools.product(topics)
        for search_term in search_terms:
            day = '2018-09-17'

            for lang in languages:
                term = ' '.join(search_term)

                try:
                    results = tweepy.Cursor(api.search, q=term,
                                geocode='28.644800,77.216721,200mi',
                                include_entities=False,count=100).pages()
                    print(term)
                    for result in results:
                        print("Searched: {} count:{} lang:{}".format(term, len(result),lang))
                        searched_tweets = [status._json for status in result]
                        rid = str(uuid.uuid4())
                        filename = 'results/{}/{} Delhi-{}-{}-{}.json'.format(key,term,rid,lang,day)
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
    return ["hi"]

def get_cities():
    return ["Delhi"]

def get_topic():
    return {"social_unrest":
            ["हमले", "विरोध", "दंगों", "पुलिस दंगों", "विद्रोह"]}

# "ouragan", "smog", "pollution", "qualité de l'air", "nourriture",
# "sécheresse", "tempête"


# 'อาชญากรรมยาเสพติด',
# 'อัตราการเกิดอาชญากรรม',
# 'กังวลด้านความปลอดภัย',
# 'การทุจริตและอาชญากรรม',
# 'อาชญากร',
# "การก่ออาชญากรรม",
# "โจมตี",
# "ความร้ายกาจ",
# "อาชญากรรม",
# "ฆาตกรรม",
# "ความไม่มั่นคง",
# "ฆาตกรรมตำรวจ"



# "रोबो","अपराध","घोर अपराध","thugs",
# "anti-vol","insecurity","insécurité",

# "crime":
# ["रोबो","अपराध","घोर अपराध","thugs",
# "anti-vol","insecurity","insécurité",
# "inseguridad","pandillas","murderers",
# "robbery","murder","assesination","mug"],
# "environment":
# ["hurricane","smog","pollution","air quality","food","droughts","dust","storm"],
# "social_unrest":
# ["Strikes","protest","riots","police riots","uprising"],
# "infrastructure":
# ['roads','electrical power','water','sanitation','airport infrastructure','bridge','Dam',
# 'water supply','sewers','electrical grids','telecommunications']

if __name__ == '__main__':
    auth = OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    start_crawl(api)

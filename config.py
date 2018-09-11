import yaml

def open_config():
    with open("secrets.yml", 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config

def get_twitter_config():
    config = open_config()

    access_token=config['twitter']['access_token']
    access_token_secret=config['twitter']['access_token_secret']
    consumer_key=config['twitter']['consumer_key']
    consumer_secret=config['twitter']['consumer_secret']
    return { 'access_token':access_token,
             'access_token_secret':access_token_secret,
             'consumer_key':consumer_key,
             'consumer_secret':consumer_secret }

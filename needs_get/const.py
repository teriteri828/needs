import datetime
import const_private
# tweet
CONSUEMR_KEY = const_private.consumer_key
CONSUEMR_SECRET = const_private.consumer_secret
ACCESS_TOKEN_KEY = const_private.access_token_key
ACCESS_TOKEN_SECRET = const_private.access_token_secret

TWEET_SEARCH = ""
TWEET_SEARCH_WORD = TWEET_SEARCH + " -filter:retweets"
TWEET_SEARCH_COUNT = 100
#前日の00:00:00になる
TWEET_SINCE_DATE = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d_00:00:00_JST')
TWEET_UNTIL_DATE = (datetime.datetime.now()).strftime('%Y-%m-%d_%H:%M:%S_JST')

# django
import os

MODEL_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../needs/"
MYSITE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../"
MYSITE_NAME = "needs_site"

# AI model

AI_MODEL_FILE = os.path.dirname(os.path.abspath(__file__)) + "/model/get_needs.h5"
USE_URL = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"

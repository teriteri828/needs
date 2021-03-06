import datetime
import const_private
import random

# tweet
CONSUEMR_KEY = const_private.consumer_key
CONSUEMR_SECRET = const_private.consumer_secret
ACCESS_TOKEN_KEY = const_private.access_token_key
ACCESS_TOKEN_SECRET = const_private.access_token_secret

TWEET_SEARCH_LIST = [
    "",
    "もっと簡単にしてほしい",
    "もっと分かりやすくしてほしい",
    "分かりにくい",
    "面倒くさい　作業",
    "改善してほしい",
    "分からない 困る",
    "疲れる",
    "時間かかる",
    "お金出してでも",
]

TWEET_SEARCH = random.choice(TWEET_SEARCH_LIST)
TWEET_SEARCH_WORD = TWEET_SEARCH + " -filter:retweets"
TWEET_SEARCH_COUNT = 100
# 前日の00:00:00になる
TWEET_SINCE_DATE = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(
    "%Y-%m-%d_00:00:00_JST"
)
TWEET_UNTIL_DATE = (datetime.datetime.now()).strftime("%Y-%m-%d_%H:%M:%S_JST")

TWEET_GEOCODE_LIST = ["34.6989741,137.7000167,20km"]
TWEET_GEOCODE = random.choice(TWEET_GEOCODE_LIST)
# django
import os

MODEL_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../needs/"
MYSITE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../"
MYSITE_NAME = "needs_site"

# AI model

AI_MODEL_FILE = os.path.dirname(os.path.abspath(__file__)) + "/model/get_needs.h5"
USE_URL = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"

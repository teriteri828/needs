# coding: UTF-8

from dataclasses import dataclass
import tweepy
import emoji
from needs_get_dto import TweetsDto
from const import (
    CONSUEMR_KEY,
    CONSUEMR_SECRET,
    ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET,
    TWEET_SEARCH_WORD,
    TWEET_SEARCH_COUNT,
    TWEET_SINCE_DATE,
    TWEET_UNTIL_DATE,
    AI_MODEL_FILE,
    USE_URL,
    TWEET_GEOCODE,
)

import tensorflow_hub as hub
import tensorflow_text
import tensorflow as tf
import numpy as np
from asari.api import Sonar

model = tf.keras.models.load_model(AI_MODEL_FILE)
embed = hub.load(USE_URL)
sonar = Sonar()


@dataclass
class TweetConnect:
    def create(self,):
        # twiteerのAPIを利用するための、認証データ作成
        auth = tweepy.OAuthHandler(CONSUEMR_KEY, CONSUEMR_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

        # twitterのAPIインスタンス生成
        twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
        return twitter_api


@dataclass
class NeedsTweetGet:
    def execute(
        self, twitter_api,
    ):
        # const.pyから取得
        search_word = TWEET_SEARCH_WORD
        search_count = TWEET_SEARCH_COUNT
        since_date = TWEET_SINCE_DATE
        until_date = TWEET_UNTIL_DATE
        geocode = TWEET_GEOCODE

        # カーソルを使用してデータ取得
        """
        if search_word == " -filter:retweets":
            search_tweets = tweepy.Cursor(
                twitter_api.search,
                q=search_word,
                lang="ja",
                since=since_date,
                until=until_date,
                geocode=geocode,
            ).items(search_count)
        else:
        """
        search_tweets = tweepy.Cursor(
            twitter_api.search,
            q=search_word,
            lang="ja",
            since=since_date,
            until=until_date,
        ).items(search_count)

        # tweetの内容を格納するためのリスト変数
        search_tweet_result = []

        # 取得したtweetの内容をリストに格納
        for search_tweet in search_tweets:
            """
            if search_word == " -filter:retweets" and search_tweet.place is None:
                continue 
            """

            if search_tweet.text[0:2] == "RT":
                continue
            search_tweet_text = search_tweet.text
            search_tweet_text = self._remove_emoji(search_tweet_text)
            if search_tweet_text[0] == "@":
                delete_word = search_tweet_text.split(" ")[0]
                # print(delete_word)
                search_tweet_text = search_tweet_text.replace(delete_word, "")

            search_tweet_datetime = search_tweet.created_at
            text_vector = embed(search_tweet_text).numpy()
            needs_bool = np.argmax(model.predict(text_vector), axis=-1)[0]
            print(
                "search_word: {}, sentence: {}".format(
                    TWEET_SEARCH_WORD, search_tweet_text
                )
            )

            nega_posi = sonar.ping(text=search_tweet_text)
            nega_posi = self._asari_unpack(nega_posi)

            search_tweet_result.append(
                TweetsDto(
                    search_tweet_text,
                    search_tweet_datetime,
                    needs_bool,
                    round(nega_posi["negative"], 2),
                    round(nega_posi["positive"], 2),
                )
            )
        return search_tweet_result

    def _remove_emoji(self, src_str):
        return "".join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

    def _asari_unpack(self, asari_result):
        asari_unpack_result = {}
        for r in asari_result["classes"]:
            asari_unpack_result[r["class_name"]] = r["confidence"]
        return asari_unpack_result

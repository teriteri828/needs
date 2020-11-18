from needs_get_entity import TweetConnect
from needs_get_entity import NeedsTweetGet
from dataclasses import dataclass
from typing import List
import datetime
from needs_get_dto import *
from needs_get_repository import DataInsert


@dataclass
class ServiceNeedsGet:
    tweet_connect: TweetConnect
    needs_tweet_get: NeedsTweetGet
    data_insert: DataInsert

    def execute(self,) -> List[TweetsDto]:
        con = self.tweet_connect.create()
        ntg = self.needs_tweet_get.execute(con)
        ngr = self.data_insert.execute(ntg)
        return ngr

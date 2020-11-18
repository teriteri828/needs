from needs_get_entity import TweetConnect, NeedsTweetGet
from needs_get_repository import DataInsert
from service_needs_get import ServiceNeedsGet

tweet_connet = TweetConnect()
needs_tweet_get = NeedsTweetGet()
data_insert = DataInsert()

needs_get = ServiceNeedsGet(tweet_connet, needs_tweet_get, data_insert)
print(needs_get.execute())

from dataclasses import dataclass
import numpy as np
import glob
from const import  USE_URL, NUM_CLASSES
import re

import tensorflow_hub as hub
import tensorflow_text
from sklearn.model_selection import train_test_split
import keras
import MeCab

embed = hub.load(USE_URL)

@dataclass
class LearnDataSplit:
    def execute(self, df_learn):
        num_classes = NUM_CLASSES

        tweets = df_learn["text"].values
        
        # データクリーン処理。精度落ちたので、いったんコメントアウト
        # sentences = []
        # for tweet in tweets:
        #     sentences.append(self._word_extract_join(tweet))
        # X = embed(sentences).numpy()


        X = embed(tweets).numpy()
        y = df_learn["needs"].values
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, random_state=123, test_size=0.2
        )

        # ラベルデータを学習用に整形
        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)

        return X_train, X_test, y_train, y_test

    def _word_extract_join(self, text):
        # 最新辞書の追加に関する参考情報
        # https://qiita.com/SUZUKI_Masaya/items/685000d569452585210c
        # https://www.saintsouth.net/blog/morphological-analysis-by-mecab-and-mecab-ipadic-neologd-and-python3/

        text = self._format_text(text)

        mecab = MeCab.Tagger(
            "-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd"
        )

        mecab.parse("")  # 文字列がGCされるのを防ぐ
        node = mecab.parseToNode(text)
        word_list = []
        while node:
            # 品詞を取得
            pos = node.feature.split(",")[0]

            if pos in ["名詞", "動詞", "形容詞", "副詞"]:
                word = node.surface
                word_list.append(word)
            # elif pos in ["動詞", "形容詞"]:
            # 次の単語に進める
            node = node.next
        ret = " ".join(word_list)
        return ret

    def _format_text(self, text):
        """
        MeCabに入れる前のツイートの整形方法例
        """

        text = re.sub(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+", "", text)
        text = re.sub("RT", "", text)
        text = re.sub("お気に入り", "", text)
        text = re.sub("まとめ", "", text)
        text = re.sub(r"[!-~]", "", text)  # 半角記号,数字,英字
        text = re.sub(r"[︰-＠]", "", text)  # 全角記号
        text = re.sub("\n", " ", text)  # 改行文字

        return text

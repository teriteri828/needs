import re

import MeCab

from dataclasses import dataclass
from needs.views.needs_dto import NeedsEntity, NeedsTopicDocument
from needs.views.stop_words import stop_words


@dataclass
class NeedsSelect:
    def all(self, models):
        needs_data_list = models.objects.all().order_by("-id")
        ret = []
        for needs in needs_data_list:
            ret.append(
                NeedsEntity(
                    nid=needs.id,
                    sentence=needs.sentence,
                    date=needs.date.replace(tzinfo=None),
                    label=needs.label,
                    negative=needs.negative,
                    positive=needs.positive,                )
            )
        return ret

    def top_limit(self, models):
        needs_data_list = models.objects.filter(label=1).order_by("-id")[:100]
        ret = []
        for needs in needs_data_list:
            ret.append(
                NeedsEntity(
                    nid=needs.id,
                    sentence=needs.sentence,
                    date=needs.date.replace(tzinfo=None),
                    label=needs.label,
                    negative=needs.negative,
                    positive=needs.positive,                )
            )
        return ret

    def search_similarity_data(self, models):
        needs_data_list = models.objects.filter(label=1).order_by("-id")[:5000]
        sentence = []
        search_data = []
        for needs in needs_data_list:
            sentence.append(needs.sentence)
            search_data.append(self._word_extract(needs.sentence))
        return sentence, search_data

    def search_contain_data(self, models, text):
        needs_data_list = models.objects.filter(
            label=1, sentence__icontains=text
        ).order_by("-id")[:5000]
        ret = []
        for needs in needs_data_list:
            ret.append(
                NeedsEntity(
                    nid=needs.id,
                    sentence=needs.sentence,
                    date=needs.date.replace(tzinfo=None),
                    label=needs.label,
                    negative=needs.negative,
                    positive=needs.positive,
                )
            )
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

    def _word_extract(self, text):
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

            if pos in ["名詞"]:
                word = node.surface
                if not word in stop_words:
                    word_list.append(word)
            # elif pos in ["動詞", "形容詞"]:
            # 次の単語に進める
            node = node.next
        ret = " ".join(word_list)
        return ret

    def topic_data(self, models):
        needs_data_list = models.objects.filter(label=1).order_by("-id")[:5000]
        ret = []
        for needs in needs_data_list:
            ret.append(NeedsTopicDocument(sentence=needs.sentence,))
        return ret

    def learn_data_get(self, models):
        needs_data_list = models.objects.all().order_by("-id")[:30]
        ret = []
        for needs in needs_data_list:
            ret.append(
                NeedsEntity(
                    nid=needs.id,
                    sentence=needs.sentence,
                    date=needs.date.replace(tzinfo=None),
                    label=needs.label,
                    negative=needs.negative,
                    positive=needs.positive,
                )
            )
        return ret

from dataclasses import dataclass, field
import MeCab
from needs.views.stop_words import stop_words
import re
from gensim import corpora, models
import numpy as np
import matplotlib

# バックエンドを指定
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64
import io


@dataclass
class TopicDocumentsAndDictionaryAndCorpus:
    def dictionary_corpus_only_create(self, needs_data_list):
        topic_documents = self._documents_create(needs_data_list)
        dictionary = corpora.Dictionary(topic_documents)
        dictionary.filter_extremes(no_below=3, no_above=0.8)
        corpus = [dictionary.doc2bow(doc) for doc in topic_documents]

        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]

        return dictionary, corpus_tfidf

    def create(self, needs_data_list):
        topic_documents = self._documents_create(needs_data_list)
        dictionary = corpora.Dictionary(topic_documents)
        corpus = [dictionary.doc2bow(doc) for doc in topic_documents]

        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]

        return topic_documents, dictionary, corpus_tfidf

    def _documents_create(self, needs_data_list):
        topic_documents = []
        for needs in needs_data_list:
            topic_word = self._word_extract(needs.sentence)
            topic_documents.append(topic_word)
        return topic_documents

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
        topic_word = []
        while node:
            # 品詞を取得
            pos = node.feature.split(",")[0]

            if pos in ["名詞"]:
                word = node.surface
                if not word in stop_words:
                    topic_word.append(word)
            elif pos in ["動詞", "形容詞"]:
                word = node.feature.split(",")[6]
                if not word in stop_words:
                    topic_word.append(word)
            # 次の単語に進める
            node = node.next
        return topic_word


@dataclass
class TopicNumberConsiderGraph:
    start: int = field(default=5)
    limit: int = field(default=15)
    step: int = field(default=1)

    def create(self, documents, dictionary, corpus):

        coherence_vals = []
        perplexity_vals = []

        for n_topic in range(self.start, self.limit, self.step):
            lda_model = models.ldamodel.LdaModel(
                corpus=corpus, id2word=dictionary, num_topics=n_topic, random_state=0
            )
            perplexity_vals.append(np.exp2(-lda_model.log_perplexity(corpus)))
            coherence_model_lda = models.CoherenceModel(
                model=lda_model,
                texts=documents,
                dictionary=dictionary,
                coherence="c_v",
            )
            coherence_vals.append(coherence_model_lda.get_coherence())

        self._create_graph(perplexity_vals, coherence_vals)
        graph = self._get_image()
        return graph

    def _create_graph(self, perplexity_vals, coherence_vals):
        plt.cla()  # グラフをリセット
        x = range(self.start, self.limit, self.step)

        fig, ax1 = plt.subplots(figsize=(12, 5))

        # coherence
        c1 = "darkturquoise"
        ax1.plot(x, coherence_vals, "o-", color=c1)
        ax1.set_xlabel("Num Topics")
        ax1.set_ylabel("Coherence", color=c1)
        ax1.tick_params("y", colors=c1)

        # perplexity
        c2 = "slategray"
        ax2 = ax1.twinx()
        ax2.plot(x, perplexity_vals, "o-", color=c2)
        ax2.set_ylabel("Perplexity", color=c2)
        ax2.tick_params("y", colors=c2)

        # Vis
        ax1.set_xticks(x)
        fig.tight_layout()

    def _get_image(self):
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode("utf-8")
        buffer.close()
        return graph


@dataclass
class TopicModel:
    def create(self, topic_number, dictionary, corpus):
        lda = models.ldamodel.LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=topic_number,
            alpha="symmetric",
            random_state=0,
        )
        return lda

    def present(self, topic_number, dictionary, corpus):
        lda = self.create(topic_number, dictionary, corpus)
        topics = []
        for topic_index in range(topic_number):
            topics.append(
                [
                    (dictionary[t[0]], t[1])
                    for t in lda.get_topic_terms(topic_index, topn=10)
                ]
            )
        return topics

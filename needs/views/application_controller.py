from django.http import HttpResponse
from django.template import loader
from gensim import corpora, models
import numpy as np
from django.http import QueryDict
import os
import csv
import pandas as pd
import datetime
import io
import matplotlib
import MeCab
import re

from needs.models import Needs
from needs.views.needs_repository import NeedsSelect
from needs.views.needs_dto import NeedsEntity
from needs.views.stop_words import stop_words

# バックエンドを指定
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64

LEARN_DATA_TEMP_FILE_PATH = os.path.dirname(
    os.path.abspath(__file__)
) + "/../../needs_learn/learn_data/learn_data_temp_{}.csv".format(
    datetime.datetime.now().strftime("%Y%m%d")
)
LEARN_DATA_FILE_PATH = (
    os.path.dirname(os.path.abspath(__file__))
    + "/../../needs_learn/learn_data/learn_data.csv"
)


def all(request):
    needs_select = NeedsSelect()
    needs_list = needs_select.all(Needs)
    template = loader.get_template("needs/needs_all_table.html")
    context = {
        "needs_list": needs_list,
    }
    return HttpResponse(template.render(context, request))


def learn(request):
    needs_select = NeedsSelect()
    needs_list = needs_select.learn_data_get(Needs)
    template = loader.get_template("needs/needs_learn_table.html")
    context = {
        "needs_list": needs_list,
    }
    return HttpResponse(template.render(context, request))


def top(request):
    needs_select = NeedsSelect()
    needs_list = needs_select.top_limit(Needs)
    template = loader.get_template("needs/needs_top_limit_table.html")
    context = {
        "needs_list": needs_list,
    }
    return HttpResponse(template.render(context, request))


def data_file_save(request):
    sentence_list = []
    label_list = []
    for key in request.GET.keys():

        label = -1

        if key == "csrfmiddlewaretoken":
            continue

        if not request.GET.get(key) == "None":
            label = int(request.GET.get(key))
        else:
            label = None

        if label == 0 or label == 1:
            nid = int(key[2:])
            print(nid)
            needs = Needs.objects.get(id=nid)
            needs.label = label
            sentence_list.append(needs.sentence)
            label_list.append(needs.label)
            needs.save()

    with open(LEARN_DATA_FILE_PATH, "a") as f:
        writer = csv.writer(f)
        for s, l in zip(sentence_list, label_list):
            writer.writerow([s, l])

    dataframe = pd.read_csv(
        LEARN_DATA_FILE_PATH, encoding="utf8", header=None, names=["text", "needs"]
    )
    dataframe = dataframe.drop_duplicates(subset="text", keep="last")
    dataframe.to_csv(LEARN_DATA_FILE_PATH, index=False)
    return HttpResponse(
        '<input type="button" value="Back" onClick="javascript:history.go(-1);">'
    )


"""
ldaの分類数を調べる用の処理
"""


def topic_words_create(text):
    #最新辞書の追加に関する参考情報
    #https://qiita.com/SUZUKI_Masaya/items/685000d569452585210c
    #https://www.saintsouth.net/blog/morphological-analysis-by-mecab-and-mecab-ipadic-neologd-and-python3/
    mecab = MeCab.Tagger("-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")

    mecab.parse("")  # 文字列がGCされるのを防ぐ
    node = mecab.parseToNode(text)
    topic_word = []
    while node:
        # 単語を取得
        word = node.surface
        # 品詞を取得
        pos = node.feature.split(",")[0]
        if pos in ["名詞"] and not word in stop_words:
            topic_word.append(word)
        # 次の単語に進める
        node = node.next
    return topic_word


# グラフ作成
def create_graph(start, limit, step, perplexity_vals, coherence_vals):
    plt.cla()  # グラフをリセット
    x = range(start, limit, step)

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


def get_image():
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph

def format_text(text):
    '''
    MeCabに入れる前のツイートの整形方法例
    '''

    text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub('RT', "", text)
    text=re.sub('お気に入り', "", text)
    text=re.sub('まとめ', "", text)
    text=re.sub(r'[!-~]', "", text)#半角記号,数字,英字
    text=re.sub(r'[︰-＠]', "", text)#全角記号
    text=re.sub('\n', " ", text)#改行文字

    return text

def topic_number_consider(request):
    needs_data_list = Needs.objects.filter(label=1).order_by("-id")[:5000]
    topic_documents = []
    for needs in needs_data_list:
        topic_word = topic_words_create(format_text(needs.sentence))
        topic_documents.append(topic_word)
    print(topic_documents)
    dictionary = corpora.Dictionary(topic_documents)
    corpus = [dictionary.doc2bow(doc) for doc in topic_documents]

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    start = 2
    limit = 22
    step = 1

    coherence_vals = []
    perplexity_vals = []

    for n_topic in range(start, limit, step):
        lda_model = models.ldamodel.LdaModel(
            corpus=corpus_tfidf, id2word=dictionary, num_topics=n_topic, random_state=0
        )
        perplexity_vals.append(np.exp2(-lda_model.log_perplexity(corpus_tfidf)))
        coherence_model_lda = models.CoherenceModel(
            model=lda_model,
            texts=topic_documents,
            dictionary=dictionary,
            coherence="c_v",
        )
        coherence_vals.append(coherence_model_lda.get_coherence())

    create_graph(start, limit, step, perplexity_vals, coherence_vals)
    graph = get_image()
    template = loader.get_template("needs/needs_topic_number_consider.html")
    context = {
        "graph": graph,
    }
    response = HttpResponse(template.render(context, request))
    return response

def topic_classify(request):

    needs_data_list = Needs.objects.filter(label=1).order_by("-id")[:5000]
    topic_documents = []
    for needs in needs_data_list:
        topic_word = topic_words_create(format_text(needs.sentence))
        topic_documents.append(topic_word)

    dictionary = corpora.Dictionary(topic_documents)
    corpus = [dictionary.doc2bow(doc) for doc in topic_documents]

    topic_number = int(request.GET.get("topic_number"))

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    lda = models.ldamodel.LdaModel(
        corpus=corpus_tfidf,
        id2word=dictionary,
        num_topics=topic_number,
        alpha="symmetric",
        random_state=0,
    )
    template = loader.get_template("needs/needs_topics.html")

    topics = []
    for topic_index in range(topic_number):
        topics.append(
            [
                (dictionary[t[0]], t[1])
                for t in lda.get_topic_terms(topic_index, topn=10)
            ]
        )
    context = {
        "topics": topics,
    }
    response = HttpResponse(template.render(context, request))

    return response

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

import tensorflow_hub as hub
import tensorflow_text

from needs.models import Needs
from needs.views.needs_repository import NeedsSelect
from needs.views.needs_dto import NeedsEntity
from needs.views.stop_words import stop_words
from needs.views.needs_topic import (
    TopicDocumentsAndDictionaryAndCorpus,
    TopicNumberConsiderGraph,
    TopicModel,
)
from needs.views.service_topic import (
    ServiceTopicNumberConsiderGraph,
    ServiceTopicClassify,
)


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
    needs_all = needs_select.all(Needs)
    template = loader.get_template("needs/needs_top_limit_table.html")
    context = {
        "needs_list": needs_list,
        "all_count": len(needs_all),
        "needs_count": len([needs for needs in needs_all if needs.label == 1]),
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
以下、トピックモデルに関する処理
"""


def topic_number_consider(request):
    needs_select = NeedsSelect()
    topic_documents_dictionary_corpus = TopicDocumentsAndDictionaryAndCorpus()
    topic_number_consider_graph = TopicNumberConsiderGraph()
    service_topic_number_consider_graph = ServiceTopicNumberConsiderGraph(
        needs_select, topic_documents_dictionary_corpus, topic_number_consider_graph
    )
    graph = service_topic_number_consider_graph.execute()

    template = loader.get_template("needs/needs_topic_number_consider.html")
    context = {
        "graph": graph,
    }
    response = HttpResponse(template.render(context, request))
    return response


def topic_classify(request):
    topic_number = int(request.GET.get("topic_number"))
    needs_select = NeedsSelect()
    topic_documents_dictionary_corpus = TopicDocumentsAndDictionaryAndCorpus()
    topic_model = TopicModel()
    service_topic_classify = ServiceTopicClassify(
        topic_number, needs_select, topic_documents_dictionary_corpus, topic_model
    )
    topics = service_topic_classify.execute()

    template = loader.get_template("needs/needs_topics.html")
    context = {
        "topics": topics,
    }
    response = HttpResponse(template.render(context, request))

    return response


"""
検索システム
"""
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")


def search_similarity(request):
    search_request = str(request.GET.get("search_request"))
    needs_select = NeedsSelect()
    sentences, search_data = needs_select.search_similarity_data(Needs)

    search_request_vector = embed(search_request)
    search_data_vectors = embed(search_data)

    similarities = np.inner(search_request_vector, search_data_vectors)
    search_result = []
    for sentence, similarity in zip(sentences, similarities[0]):
        if similarity > 0.5 and len(sentence) > 15:
            search_result.append([sentence, similarity])
    template = loader.get_template("needs/needs_search_similarity.html")
    context = {
        "search_request": search_request,
        "search_similarity_result": search_result,
    }
    response = HttpResponse(template.render(context, request))

    return response


def search_contain(request):
    search_request = str(request.GET.get("search_request"))
    needs_select = NeedsSelect()
    search_result = needs_select.search_contain_data(Needs, search_request)

    template = loader.get_template("needs/needs_search_contain.html")
    context = {
        "search_request": search_request,
        "search_contain_result": search_result,
    }
    response = HttpResponse(template.render(context, request))

    return response


"""
データベースへのインポート、エクスポート
"""

import csv
from io import TextIOWrapper, StringIO
from asari.api import Sonar
sonar = Sonar()
import tensorflow as tf

AI_MODEL_FILE = os.path.dirname(os.path.abspath(__file__)) + "/../../needs_get/model/get_needs.h5"
print(AI_MODEL_FILE)
model = tf.keras.models.load_model(AI_MODEL_FILE)

def upload(request):
    if "csv" in request.FILES:
        form_data = TextIOWrapper(request.FILES["csv"].file, encoding="utf-8")
        csv_file = csv.reader(form_data)
        for line in csv_file:
            sentence = line[0]
            date = line[1]
            needs_obj = Needs.objects.filter(sentence=sentence)
            if len(needs_obj) > 0:
                continue

            #needs label
            text_vector = embed(sentence).numpy()
            needs_bool = np.argmax(model.predict(text_vector), axis=-1)[0]

            #nega_posi
            nega_posi = sonar.ping(text=sentence)
            nega_posi = _asari_unpack(nega_posi)
            n = Needs(
                sentence=sentence,
                date=date,
                label=needs_bool,
                negative=round(nega_posi["negative"], 2),
                positive=round(nega_posi["positive"], 2),
            )
            n.save()

    template = loader.get_template("needs/upload.html")
    context = {}
    response = HttpResponse(template.render(context, request))

    return response



def download(request):
    return request

def _asari_unpack(asari_result):
    asari_unpack_result = {}
    for r in asari_result["classes"]:
        asari_unpack_result[r["class_name"]] = r["confidence"]
    return asari_unpack_result
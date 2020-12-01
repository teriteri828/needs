from django.http import HttpResponse
from django.template import loader
from needs.models import Needs
from needs.views.needs_repository import NeedsSelect
from needs.views.needs_dto import NeedsEntity
from django.http import QueryDict
import os
import csv
import pandas as pd
import datetime

LEARN_DATA_TEMP_FILE_PATH = (
    os.path.dirname(os.path.abspath(__file__))
    + "/../../needs_learn/learn_data/learn_data_temp_{}.csv".format(datetime.datetime.now().strftime('%Y%m%d'))
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
    return HttpResponse('<input type="button" value="Back" onClick="javascript:history.go(-1);">')

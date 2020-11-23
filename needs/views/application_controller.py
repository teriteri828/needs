from django.http import HttpResponse
from django.template import loader
from needs.models import Needs
from needs.views.needs_repository import NeedsSelect
from needs.views.needs_dto import NeedsEntity


def all(request):
    needs_select = NeedsSelect()
    needs_list = needs_select.all(Needs)
    template = loader.get_template("needs/needs_all_table.html")
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
    #print(request)
    print(request.GET.get('nid_10'))
    return HttpResponse("aa")
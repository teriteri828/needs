from django.urls import path

from needs.views import application_controller

app_name = 'needs'
urlpatterns = [
    path('', application_controller.index, name='index'),
]
from django.urls import path

from needs.views import application_controller

app_name = 'needs'
urlpatterns = [
    path('all', application_controller.all, name='all'),
    path('top', application_controller.top, name='top'),
]
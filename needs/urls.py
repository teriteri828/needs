from django.urls import path

from needs.views import application_controller

app_name = 'needs'
urlpatterns = [
    path('all', application_controller.all, name='all'),
    path('top', application_controller.top, name='top'),
    path('learn', application_controller.learn, name='learn'),
    path('data_file_save', application_controller.data_file_save, name='data_file_save'),
]
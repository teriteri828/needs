from django.urls import path

from needs.views import application_controller

app_name = 'needs'
urlpatterns = [
    path('all', application_controller.all, name='all'),
    path('top', application_controller.top, name='top'),
    path('learn', application_controller.learn, name='learn'),
    path('data_file_save', application_controller.data_file_save, name='data_file_save'),
    path('topic_number_consider', application_controller.topic_number_consider, name='topic_number_consider'),
    path('topic_classify', application_controller.topic_classify, name='topic_classify'),
    path('search_similarity', application_controller.search_similarity, name='search_similarity'),
    path('search_contain', application_controller.search_contain, name='search_contain'),
]
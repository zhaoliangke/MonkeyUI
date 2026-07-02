from django.urls import path
from apps.crawler import views

urlpatterns = [
    path('test-connect', views.test_connect),
    path('start', views.start_crawl),
    path('progress', views.task_progress),
    path('task/list', views.task_list),
    path('result/save', views.result_save),
]

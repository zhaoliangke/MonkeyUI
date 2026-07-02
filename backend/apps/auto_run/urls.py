from django.urls import path
from apps.auto_run import views

urlpatterns = [
    path('execute', views.run_execute),
    path('batch', views.run_batch),
    path('record/list', views.record_list),
    path('record/detail', views.record_detail),
]

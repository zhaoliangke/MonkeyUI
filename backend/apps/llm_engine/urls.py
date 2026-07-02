from django.urls import path
from apps.llm_engine import views

urlpatterns = [
    path('config/save', views.config_save),
    path('config/test', views.config_test),
    path('template/list', views.template_list),
    path('template/save', views.template_save),
    path('generate/script', views.generate_script),
    path('log/list', views.log_list),
]

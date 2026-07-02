from django.urls import path
from apps.environment import views

urlpatterns = [
    path('env/list', views.env_list),
    path('env/save', views.env_save),
    path('credential/list', views.credential_list),
    path('credential/save', views.credential_save),
]

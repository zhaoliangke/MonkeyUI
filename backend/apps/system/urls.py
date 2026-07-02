from django.urls import path
from apps.system import views

urlpatterns = [
    path('user/list', views.user_list),
    path('user/save', views.user_save),
    path('role/list', views.role_list),
    path('role/save', views.role_save),
    path('setting/get', views.setting_get),
    path('setting/save', views.setting_save),
    path('log/list', views.log_list),
]

from django.urls import path
from apps.reflux import views

urlpatterns = [
    path('list', views.reflux_list),
    path('detail', views.reflux_detail),
    path('audit', views.reflux_audit),
    path('rollback', views.reflux_rollback),
]

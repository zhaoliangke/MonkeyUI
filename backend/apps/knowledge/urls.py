from django.urls import path
from apps.knowledge import views

urlpatterns = [
    path('category/list', views.category_list),
    path('category/save', views.category_save),
    path('asset/list', views.asset_list),
    path('asset/save', views.asset_save),
    path('asset/detail/<int:asset_id>', views.asset_detail),
    path('asset/batch', views.asset_batch),
    path('script/save', views.script_save),
    path('version/diff', views.version_diff),
    path('dashboard/stats', views.dashboard_stats),
]

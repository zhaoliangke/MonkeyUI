from django.urls import path
from apps.project import views

urlpatterns = [
    path('list', views.project_list),
    path('save', views.project_save),
    path('set-default', views.project_set_default),
    path('permission/save', views.project_permission_save),
    path('members/<int:project_id>', views.project_members),
    path('delete', views.project_delete),
]

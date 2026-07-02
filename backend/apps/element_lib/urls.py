from django.urls import path
from apps.element_lib import views

urlpatterns = [
    path('list', views.element_list),
    path('save', views.element_save),
    path('repair', views.element_repair),
    path('related-cases', views.element_related_cases),
]

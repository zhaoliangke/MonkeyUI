from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/project/', include('apps.project.urls')),
    path('api/llm/', include('apps.llm_engine.urls')),
    path('api/knowledge/', include('apps.knowledge.urls')),
    path('api/crawler/', include('apps.crawler.urls')),
    path('api/env/', include('apps.environment.urls')),
    path('api/element/', include('apps.element_lib.urls')),
    path('api/run/', include('apps.auto_run.urls')),
    path('api/reflux/', include('apps.reflux.urls')),
    path('api/system/', include('apps.system.urls')),
]

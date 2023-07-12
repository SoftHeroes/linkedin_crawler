from django.urls import path
from . import views

urlpatterns = [
    path('crawl-profiles/', views.crawl_profiles, name='crawl_profiles'),
    path('crawl-peoples/', views.crawl_peoples, name='crawl_peoples'),
]
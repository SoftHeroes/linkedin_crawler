from django.urls import path
from . import views

urlpatterns = [
    path('crawlers/', views.crawlers, name='crawlers'),
]
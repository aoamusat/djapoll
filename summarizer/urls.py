from django.conf.urls import url
from summarizer import views

urlpatterns = [
 url(r'^$', views.index, name='index'),
 url(r'^summarize/', views.summarize, name='summarize'),
]
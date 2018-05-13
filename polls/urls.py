from django.conf.urls import url
from polls import views
from django.contrib.auth.decorators import login_required

app_name = 'polls'

urlpatterns = [
	url(r'^$', login_required(views.IndexView.as_view()), name='index'),
	url(r'^(?P<pk>[0-9]+)/$', login_required(views.DetailView.as_view()), name='detail'),
	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
	url(r'^election/result/$', views.ElectionResultsView.as_view(), name='election_result'),
	url(r'^login/$', views.show_login, name='login'),
	url(r'^login/attempt/$', views.attempt_login, name='attempt_login'),
	url(r'^logout/$', views.do_logout, name='logout'),
	url(r'^vote/$', views.vote_, name='vote_'),
]

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from polls.models import Question, Choice
from django.db.models import F
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class IndexView(generic.ListView):
	"""Docstring for IndexView"""
	template_name = "polls/index.html"
	context_object_name = "latest_questions"

	def get_queryset(self):
		"""Return the last five polls"""
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
			

class DetailView(generic.DetailView):
	"""docstring for DetailView"""
	model = Question
	template_name = "polls/detail.html"
	
class ResultsView(generic.DetailView):
	"""docstring for ResultsView"""
	model = Question
	template_name = "polls/results.html"
		
class ElectionResultsView(generic.ListView):
	"""docstring for ElectionResultView"""
	context_object_name = "questions"
	template_name = "polls/election_result.html"
	
	def get_queryset(self):
		return Question.objects.all().order_by('id')

def show_login(request):
	template = loader.get_template('polls/login.html')
	return HttpResponse(template.render({}, request))

def vote_(request):
	return HttpResponse(request.POST)
	pass

def vote(request, question_id):
	question = Question.objects.get(pk = question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		template = loader.get_template('polls/detail.html')
		return HttpResponse(template.render({'question': question}, request))
	else:
		selected_choice.votes = F('votes') + 1  # avoids race condition
		selected_choice.save()
		logout(request)
		return HttpResponseRedirect(reverse('polls:index'))

def attempt_login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(reverse('polls:index'))
	else:
		return HttpResponseRedirect(reverse('polls:login'))

def do_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('polls:login'))
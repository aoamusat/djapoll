from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template

import Algorithmia

# Create your views here.

def index(request):
	template = get_template('summarizer/index.html')
	return HttpResponse(template.render({}, request))

def summarize(request):
	_input = request.POST['text_input']
	client = Algorithmia.client('simpjKSYTfqHFpp/lOw4ViLFeTo1')
	algorithm = client.algo('nlp/Summarizer/0.1.6')
	response = algorithm.pipe(_input)
	return HttpResponse(response.result)
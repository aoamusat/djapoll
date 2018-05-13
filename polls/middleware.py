from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

class LoginMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if not request.user.is_authenticated():
			return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))
		else:
			pass
		response = self.get_response(request)
		return response
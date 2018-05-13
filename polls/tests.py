import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from django.urls import reverse

# helper methods

def create_question(question_text, days):
		"""
		create a new question with question text and published the given number of days
		from now offset. For past days, use -ve for published question. +ve for questions
		yet to be published. 
		"""
		time = timezone.now() + datetime.timedelta(days=days)
		Question.objects.create(question_text=question_text, pub_date=time)

# Create your tests here.

class QuestionMethodTests(TestCase):
	"""docstring for QuestionMethodTests"""
	def test_was_published_recently_with_future_question(self):
		""" 
		The method was_published_rececntly() of the Question class
		should return False for questions whose date is in the future
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		""" 
		The method was_published_rececntly() of the Question class
		should return False for questions whose date is older than 1 day
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		""" 
		The method was_published_rececntly() of the Question class 
		should return False for questions whose date is older than 1 day
		"""
		time = timezone.now() + datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), False)


class QuestionViewTests(TestCase):
	"""docstring for QuestionViewTests"""
	def test_index_view_with_no_questions(self):
		"""
		An appropriate message should be displayed if
		no question exists
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No polls available')
		self.assertQuerysetEqual(response.context['latest_questions'], [])

	def test_index_view_with_past_question(self):
		"""
		Questions with the pub_date should be displayed on the index page
		"""
		create_question(question_text="Past Question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_questions'],
			['<Question: Past Question.>']
		)

	def test_index_view_with_future_question(self):
		"""
		Questions with the pub_date in the future should not be displayed on the index page
		"""
		create_question(question_text="Future Question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls available")
		self.assertQuerysetEqual(
			response.context['latest_questions'],
			[]
		)

	def test_index_view_with_future_question_and_past_question(self):
		"""
		Questions with the pub_date in the past should only be displayed
		"""
		create_question(question_text="Future Question.", days=30)
		create_question(question_text="Past Question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_questions'],
			['<Question: Past Question.>']
		)

	def test_index_view_with_two_past_question(self):
		"""
		Questions with the pub_date in the past should only be displayed
		"""
		create_question(question_text="Past Question 1.", days=-30)
		create_question(question_text="Past Question 2.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_questions'],
			['<Question: Past Question 1.>', '<Question: Past Question 2.>']
		)


class QuestionIndexDetailTests(TestCase):
	"""docstring for QuestionIndexDetailTests"""
	
	def test_detail_view_with_a_future_question(self):
		"""
		The detail view of a question with a pub_date in the
		future should return a 404 not found
		"""
		future_question = create_question(question_text='Future Question.', days=5)
		url = reverse('polls:detail', args=(future_question.id, ))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)
		
	def test_detail_view_with_a_past_question(self):
		"""
		The detail view of a question with a pub_date in the past should
		display the question's text.
		"""
		past_question = create_question(question_text='Past Question.', days=-5)
		url = reverse('polls:detail', args=(past_question.id, ))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)

class ElectionResultsTests(TestCase):
	all_questions = Question.objects.all().order_by('id');
	for question in all_questions:
		print(question.question_text)
		for choice in question.choice_set.all():
			print("%s => %s votes" % (choice.choice_text, choice.votes))
	


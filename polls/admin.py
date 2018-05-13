from django.contrib import admin
from polls import models

# Register your models here.

class ChoiceInline(admin.TabularInline):
	model = models.Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	"""docstring for QuestionAdmin"""
	inlines = [ChoiceInline]
	list_display = ('question_text', 'pub_date', 'was_published_recently')
		


admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Choice)
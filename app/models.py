from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from datetime import date


# Create your models here.

class Quiz(models.Model):
	name = models.CharField(max_length=100,blank=True,null=True)
	image = models.ImageField(upload_to='images/')
	no_of_questions = models.IntegerField()
	total_mark=models.IntegerField()
	pass_mark=models.IntegerField(default=0)
	api = models.CharField(max_length=450)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("instruction",kwargs={'id':self.id})	

	def get_absolute_test_url(self):
		return reverse("test",kwargs={'id':self.id})

	def get_absolute_test_object_create_url(self):
		return reverse("test_questions_creation",kwargs={'id':self.id})			

	def get_question_mark(self):
		return self.total_mark // self.no_of_questions


class Quiz_questions(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	quiz_type = models.ForeignKey(Quiz,on_delete=models.CASCADE)
	question=models.CharField(max_length=500)
	option1=models.CharField(max_length=100)
	option2=models.CharField(max_length=100)
	option3=models.CharField(max_length=100)
	answer=models.CharField(max_length=100)
	user_answer=models.CharField(max_length=100,default='not answered')
	date = models.DateTimeField(auto_now_add=True)
	status=models.BooleanField(default=False)


	def __str__(self):
		return self.question

class Quiz_records(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	quiz_type=models.ForeignKey(Quiz,on_delete=models.CASCADE)
	marks=models.IntegerField(default=0)
	result=models.BooleanField(default=False)
	question=models.ManyToManyField(Quiz_questions)
	completion_status=models.BooleanField(default=False)

	def __str__(self):
		return self.user.username
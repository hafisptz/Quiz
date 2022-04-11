from django.shortcuts import render,redirect
from .models import Quiz,Quiz_questions,Quiz_records
from django.contrib.auth.decorators import login_required
import requests
import random
from django.views.generic import ListView,DetailView

# Create your views here.

#home
class HomeView(ListView):
	model = Quiz
	paginate_by = 6
	template_name = "home.html"



@login_required
def instruction(request,id):
	quiz_item=Quiz.objects.get(id=id)
	return render(request,'instruction.html',{'item':quiz_item})

	
Test=True
def test_question_create(request,id):
	old_quiz_qustions=Quiz_questions.objects.filter(user=request.user,status=False)
	if old_quiz_qustions:
		for i in range(len(old_quiz_qustions)):
			old_quiz_qustions[i].status=True
			old_quiz_qustions[i].save()
	old_quiz_records=Quiz_records.objects.filter(user=request.user,completion_status=False)
	if old_quiz_records:
		for i in range(len(old_quiz_records)):
			old_quiz_records[i].completion_status=True
			old_quiz_records[i].save()
	quiz=Quiz.objects.get(id=id)	
	api=quiz.api
	json_data = requests.get(api).json
	no_of_questions = quiz.no_of_questions
	for i in range(0,no_of_questions):
		print(i)
		obj=Quiz_questions.objects.create(user=request.user,quiz_type=quiz)
		ques=json_data()['results'][i]['question']
		print(ques)
		obj.question=ques
		options=(json_data()['results'][i]['incorrect_answers'])
		obj.option1=options[0]
		obj.option2=options[1]
		obj.option3=options[2]
		answer_option=(json_data()['results'][i]['correct_answer'])
		obj.answer=answer_option
		obj.save()

	return redirect('test',id=id)	
	

	


def test(request,id):
	if request.method =='POST':
		quiz=Quiz.objects.get(id=id)
		user_answer=request.POST.get('btn')
		print(user_answer)
		questions=Quiz_questions.objects.filter(user=request.user,quiz_type=quiz,status=False)
		qno=questions.count()
		qno=quiz.no_of_questions-(qno-1)
		if questions:
			obj=questions[0]
			print(obj.answer)
			if user_answer==obj.answer:
				print("You clicked correct answer")
				Quiz_record,created=Quiz_records.objects.get_or_create(user=request.user,quiz_type=quiz,completion_status=False)
				score=quiz.total_mark // quiz.no_of_questions
				print(score)
				Quiz_record.marks =Quiz_record.marks + score
				print(quiz.total_mark)
				Quiz_record.question.add(obj.id)
				Quiz_record.save()

			else:
				print("You clicked wrong answer")
				Quiz_record,created=Quiz_records.objects.get_or_create(user=request.user,quiz_type=quiz,completion_status=False)
				Quiz_record.question.add(obj.id)
				Quiz_record.save()	
			obj.status=True
			obj.save()
		
	quiz=Quiz.objects.get(id=id)

	questions=Quiz_questions.objects.filter(user=request.user,quiz_type=quiz,status=False)
	qno=questions.count()
	qno=quiz.no_of_questions-(qno-1)
	if questions:
		question=questions[0]
		print(question.status)
		options=[]
		options.append(question.option1)
		options.append(question.option2)
		options.append(question.option3)
		ans=question.answer
		print(ans)
		pos=random.choice(range(0,4))
		options.insert(pos,ans)
		question.save()


		return render(request,'test.html',{'question':question,'options':options,'ans':ans,'quiz':quiz,'qno':qno})
	else:
		Quiz_record=Quiz_records.objects.get(user=request.user,quiz_type=quiz,completion_status=False)
		Quiz_record.completion_status=True
		if Quiz_record.marks >= quiz.pass_mark:
			Quiz_record.result=True
		Quiz_record.save()
		return redirect('result',id=id)

def result(request,id):
	quiz=Quiz.objects.get(id=id)
	Quiz_record=Quiz_records.objects.filter(user=request.user,quiz_type=quiz,completion_status=True).last()
	if Quiz_record:
		Quiz_record=Quiz_record

		context={

		'quiz_record':Quiz_record,
		'quiz':quiz,
		}


	return render(request,'result.html',context)
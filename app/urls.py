from django.urls import path
from .views import *

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('instruction/<id>',instruction,name='instruction'),
    path('test_object_create/<id>',test_question_create,name='test_questions_creation'),
    path('test/<id>',test,name='test'),
    path('result/<id>',result,name='result'),

    
]

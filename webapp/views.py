from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    question_id = "Mjaw"
    return HttpResponse("You're looking at question %s." % question_id)
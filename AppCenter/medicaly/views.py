from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def hello(requests):
    return JsonResponse("hello!", safe=False)

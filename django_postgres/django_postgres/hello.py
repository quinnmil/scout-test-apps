from django.http import HttpResponse

def hello(request): 
    return HttpResponse("Hello world!")

def entry(request): 
    return HttpResponse("Welcome")
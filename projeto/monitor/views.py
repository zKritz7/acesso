from django.shortcuts import render

# Create your views here.

def index(request):
    template = "index.html"
    return render(request, template)

def new(request):
    template = "new.html"
    return render(request, template)
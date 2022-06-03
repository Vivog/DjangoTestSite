from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def home(request):
    output = "<h3><a href = 'admin/'>Admin></a></h3>"
    return HttpResponse(output)

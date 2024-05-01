from django.shortcuts import render
from django.http import HttpResponse

def test_route(request):
    return render(request, 'projects/projects.html')

def test_route1(request, pk):
    return render(request, 'projects/test.html')


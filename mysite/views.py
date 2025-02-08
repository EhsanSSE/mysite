# views.py
from django.shortcuts import render

def coming_soon(request):
    return render(request, 'coming-soon.html')
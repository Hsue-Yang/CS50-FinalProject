from django.shortcuts import render
from django.http import HttpResponse

# request -> response
def home(request):
    return render(request, 'home.html', {
        'title': 'Home Page',
        'message': 'Welcome to the Shopping App!'
    })
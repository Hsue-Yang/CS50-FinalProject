from django.shortcuts import render
from django.http import HttpResponse

# request -> response
def home(request):
    return render(request, 'home.html', {
        'title': 'Home Page',
        'message': 'Welcome to the Shopping App!'
    })

def index(request):
    selected_stores = request.session.get('selected_stores', [])
    return render(request, 'index.html', {'selected_stores': selected_stores})

def search(request):
    query = request.GET.get('query', '')
    if query:
        # Simulate a search result
        results = [f"Result {i} for '{query}'" for i in range(1, 6)]
    else:
        results = []
    
    return render(request, 'search.html', {'query': query, 'results': results})
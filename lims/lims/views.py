from django.http import HttpResponse
from django.shortcuts import render_to_response
from records.models import Book


def search(request):
    errors = []
    if 'query' in request.GET and 'scope' in request.GET:
        query = request.GET['query']
        scope = request.GET['scope']
        if not query:
            errors.append('Enter a search term.')
        elif not scope:
            errors.append('Select a search scope.')
        elif scope == 'Title':
            books = Book.objects.filter(name__icontains=query)
        elif scope == 'Author':
            books = Book.objects.filter(authors__icontains=query)
        elif scope == 'Subject':
            books = Book.objects.filter(authors__icontains=query)
        elif scope == 'ISBN':
            books = Book.objects.filter(isbn__icontains=query)
        else:
            errors.append('Unregonized search scope.')
    return render_to_response('search.html', locals())

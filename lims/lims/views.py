from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from records.models import Book
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test


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

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if 'next' in request.GET:
                redirect = request.GET['next']
            else:
                redirect = '/loggedin/'
            return HttpResponseRedirect(redirect)
        else:
            return render_to_response('login.html', {'error':True})
    return render_to_response('login.html')

@login_required(login_url = '/login/')
def loggedin(request):
    return render_to_response('loggedin.html', {'user':request.user})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

def is_normal_user_logged_in(user):
    if not user.is_authenticated():
        return False
    groups = user.groups.all()
    for i in range(len(groups)):
        if groups[i].name == 'NormalUser':
            return True
    return False

@user_passes_test(is_normal_user_logged_in, login_url = '/login')
def need_normal_user_logged_in(request):
    return render_to_response('user_passes_test.html')

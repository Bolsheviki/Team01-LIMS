from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from records.models import Book
from django.contrib import auth
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required, user_passes_test

Per_Page = 1

def get_books(scope, query):
    if scope == 'Title':
        books = Book.objects.filter(name__icontains=query)
    elif scope == 'Author':
        books = Book.objects.filter(authors__icontains=query)
    elif scope == 'ISBN':
        books = Book.objects.filter(isbn=query)
    return books


def search_base(request):
    return render_to_response('search-base.html')


def search(request):
    errors = []
    
    p = request.GET.get('page', '1')
    if not p.isdigit():
        p = 1
    else:
        p = int(p)

    if 'query' in request.POST and 'scope' in request.POST:
        query = request.POST['query']
        scope = request.POST['scope']
        request.session['query'] = query
        request.session['scope'] = scope
    elif 'query' in request.session and 'scope' in request.session: 
        query = request.session['query']
        scope = request.session['scope']
    else:
        return HttpResponseRedirect('/search-base/')

    book_list = get_books(scope, query)

    return list_detail.object_list(
        request,
        paginate_by = Per_Page,
        page = p,
        queryset = book_list,
        template_name = 'search.html',
        template_object_name = 'book',
    )


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
	
def is_in_group(user, groupname):
    return user.groups.filter(name = groupname).count() > 0

def is_normal_user_logged_in(user):
    return user.is_authenticated() and is_in_group(user, 'NormalUser')

@user_passes_test(is_normal_user_logged_in, login_url = '/login')
def need_normal_user_logged_in(request):
    return render_to_response('user_passes_test.html')

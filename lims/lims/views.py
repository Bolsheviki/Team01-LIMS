from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required, user_passes_test
from lims.forms import SearchForm
from lims import util

Per_Page = 1


def search_in_template(request, template_name, app):
    
    if 'scope' not in request.GET or 'query' not in request.GET:
        form = SearchForm()
        return render_to_response(template_name, locals())
    
    scope = request.GET.get('scope', 'T')
    query = request.GET.get('query', '')
    
    form = SearchForm(request.GET)
    
    p = request.GET.get('page', '1')
    if not p.isdigit():
        p = 1
    else:
        p = int(p)

    if not form.is_valid():
        return render_to_response(template_name, locals())

    q = form.cleaned_data
    book_list = util.get_books(scope, query)
    basic_info = { 'form': form, 'scope': scope, 'query': query, 'app': app }

    return list_detail.object_list(
        request,
        paginate_by = Per_Page,
        page = p,
        queryset = book_list,
        template_name = template_name,
        template_object_name = 'book',
        extra_context = basic_info,
    )

    
def info_book_in_template(request, isbn, template_name):
    book = util.get_book_info(isbn)
    return render_to_response(template_name, locals());


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

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.generic import list_detail
from lims.forms import SearchForm, LoginForm, SettingsForm
from lims import util

Per_Page = 1


def search_in_template(request, template_name, app):
    user = request.user
    
    if 'scope' not in request.GET or 'query' not in request.GET:
        form = SearchForm()
        is_begin = True
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
    return render_to_response(template_name, locals(), context_instance=RequestContext(request));


def login_in_template(request, group_name, template_name, redirect_url, login_check_method):
    login_check = login_check_method(request.user)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        post = {'username':username, 'password':password, 'group_name':group_name}
        form = LoginForm(post)
        
        if form.is_valid():
            user = auth.authenticate(username = username, password = password)
            auth.login(request, user)
            if 'next' in request.GET:
                redirect = request.GET['next']
            else:
                redirect = redirect_url
            return HttpResponseRedirect(redirect)
        else:
#<<<<<<< HEAD
            return render_to_response('login.html', {'error':True})
    return render_to_response('login.html', {'error':True})

@login_required(login_url = '/login/')
def loggedin(request):
    return render_to_response('loggedin.html', {'user':request.user})
#=======
            return render_to_response(template_name, {'form' : form, 'login_check':login_check }, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        return render_to_response(template_name, { 'form' : form, 'login_check':login_check }, context_instance=RequestContext(request))
#>>>>>>> f56d96a42d067d3312366ea5167f4723bc841356

		
def logout_in_template(request, redirect_url):
    auth.logout(request)
    return HttpResponseRedirect(redirect_url)

def settings_in_template(request, template_name):
    if request.method == 'POST':
        form = SettingsForm(request.POST)

        if form.is_valid():
            if request.POST.get('need_reset_password', False):
                request.user.set_password(request.POST['password_first'])
            request.user.email = request.POST['email']
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.save()
            is_set = True

    else:
        dict = {}
        dict['password_first'] = ''
        dict['password_confirm'] = ''
        dict['email'] = request.user.email
        dict['first_name'] = request.user.first_name
        dict['last_name'] = request.user.last_name
        form = SettingsForm(dict)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

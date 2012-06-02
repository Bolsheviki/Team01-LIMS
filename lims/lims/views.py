from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required, user_passes_test
from lims.forms import SearchForm, LoginForm
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


def login_in_template(request, group_name, template_name, redirect_url):
    form = LoginForm()
    if request.method == 'POST':      
        username = request.POST.get('username', '')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render_to_response(template_name, {'form' : form, 'errors' : 'User not exist!'})
        
        if not is_in_group(user, group_name):
            return render_to_response(template_name, {'form' : form, 'errors' : 'User not belong to specific group!'})
        
        password = request.POST.get('password', '')
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if 'next' in request.GET:
                redirect = request.GET['next']
            else:
                redirect = redirect_url
            return HttpResponseRedirect(redirect)
        else:
            return render_to_response(template_name, {'form' : form, 'errors' : 'Password not matched!'})
        
    return render_to_response(template_name, { 'form' : form })

#@login_required(login_url = '/login/')
#def loggedin(request):
#    return render_to_response('loggedin.html', {'user':request.user})

def logout_in_template(request, redirect_url):
    auth.logout(request)
    return HttpResponseRedirect(redirect_url)

def is_in_group(user, group_name):
    return user.groups.filter(name = group_name).count() > 0

def is_normal_user_logged_in(user):
    return user.is_authenticated() and is_in_group(user, 'NormalUser')

#@user_passes_test(is_normal_user_logged_in, login_url = '/login')
#def need_normal_user_logged_in(request):
#    return render_to_response('user_passes_test.html')

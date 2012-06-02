# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from lims.views import login_in_template, logout_in_template
from user_admin.forms import SearchForm
from user_admin import util
    
def login(request):
    return login_in_template(request, 'UserAdmin', 'user_admin/login.html', '/user-admin')

def logout(request):
    return logout_in_template(request, '/user-admin/login')

Per_Page = 1

def search(request):
    template_name = 'user_admin/search.html'
    
    if 'scope' not in request.GET or 'query' not in request.GET:
        form = SearchForm()
        return render_to_response(template_name, locals())
    
    scope = request.GET.get('scope', 'N')
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
    user_list = util.get_users(scope, query)
    return list_detail.object_list(
        request,
        paginate_by = Per_Page,
        page = p,
        queryset = user_list,
        template_name = template_name,
        template_object_name = 'user',
        extra_context = { 'form': form, 'scope': scope, 'query': query, 'show_result':True },
    )
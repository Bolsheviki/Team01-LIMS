# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from lims.views import login_in_template, logout_in_template
from user_admin.forms import SearchForm, UserInfoForm
from user_admin import util
from lims.util import is_in_group, is_user_admin_logged_in
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
    
def login(request):
    return login_in_template(request, 'UserAdmin', 'user_admin/login.html', '/user-admin')

def logout(request):
    return logout_in_template(request, '/user-admin/login')

Per_Page = 1

@user_passes_test(is_user_admin_logged_in, login_url = '/user-admin/login')
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

@user_passes_test(is_user_admin_logged_in, login_url = '/user-admin/login')
def info_user(request, username):
    try:
        user = User.objects.get(username=username)
        is_normal_user = is_in_group(user, 'NormalUser')
        profile = user.get_profile()

        if request.method == 'POST':
            form = UserInfoForm(request.POST)
            if form.is_valid():
                post = request.POST
                user.email = request.POST['email']
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                if 'level' in request.POST:
                    profile.level = request.POST['level']
                if 'debt' in request.POST:
                    profile.debt = request.POST['debt']
                profile.save()
                user.save()
                is_set = True
        else:
            user_dict = { 'email':user.email, 'first_name':user.first_name, 'last_name':user.last_name,
                          'level':profile.level, 'debt':profile.debt }
            form = UserInfoForm(user_dict)


        return render_to_response('user_admin/info_user.html', locals())
    
    except User.DoesNotExist:
        return render_to_response('user_admin/info_user.html')
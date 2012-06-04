# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django.template import RequestContext
from lims.views import login_in_template, logout_in_template, settings_in_template
from user_admin.forms import SearchForm, UserInfoForm, BatchUserForm
from user_admin import util
from db.models import UserProfile
from lims.util import is_in_group, is_user_admin_logged_in
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
    
    
def login(request):
    return login_in_template(request, 'UserAdmin', 'user_admin/login.html', '/user-admin', is_user_admin_logged_in, 'user-admin')

    
def logout(request):
    return logout_in_template(request, '/user-admin/login')

    
Per_Page = 1


@user_passes_test(is_user_admin_logged_in, login_url = '/user-admin/login')
def search(request):
    app = 'user-admin'
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

    user_list = util.get_users(scope, query)
    basic_info = { 'form': form, 'scope': scope, 'query': query, \
                    'show_result': True, 'app': app }
                    
    return list_detail.object_list(
        request,
        paginate_by = Per_Page,
        page = p,
        queryset = user_list,
        template_name = template_name,
        template_object_name = 'user',
        extra_context = basic_info,
    )

    
@user_passes_test(is_user_admin_logged_in, login_url = '/user-admin/login')
def settings(request):
    return settings_in_template(request, 'user_admin/settings.html', 'user-admin')

    
@user_passes_test(is_user_admin_logged_in, login_url = '/user-admin/login')
def info_user(request, username):
    app = 'user-admin'
    try:
        user = User.objects.get(username=username)
        is_normal_user = is_in_group(user, 'NormalUser')
        if is_normal_user:
            profile = user.get_profile()

        if request.method == 'POST':
            form = UserInfoForm(request.POST)
            if form.is_valid():
                if request.POST.get('need_reset_password', False):
                    user.set_password(request.POST['password_first'])
                user.email = request.POST['email']
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                    
                if is_normal_user:
                    profile.level = request.POST['level']
                    profile.debt = int(request.POST['debt'])
                    profile.save()
                user.save()
                is_set = True
        else:
            user_dict = { 'email':user.email, 'first_name':user.first_name, 'last_name':user.last_name }
            user_dict['password_first'] = ''
            user_dict['password_last'] = ''
            if is_normal_user:
                user_dict['level'] = profile.level
                user_dict['debt'] = profile.debt 
            form = UserInfoForm(user_dict)

        return render_to_response('user_admin/info_user.html', locals(), context_instance=RequestContext(request))
    
    except User.DoesNotExist:
        return render_to_response('user_admin/info_user.html', locals(), context_instance=RequestContext(request))

        
def batch_user_handle(request, template_name, handle_func):
    app = 'user-admin'
    if request.method == 'POST':
        form = BatchUserForm(request.POST)
        if form.is_valid():
            todo_list = []
            batch_username = request.POST['batch_username']
            from_index = int(request.POST['from_index'])
            to_index = int(request.POST['to_index'])
            wildcard_length = int(request.POST['wildcard_length'])
            level = request.POST['level']
            group_name = request.POST['group']
            for index in range(from_index, to_index + 1):
                todo_list.append(batch_username.replace(r'(*)', str(index).zfill(wildcard_length)))
                
            just_list_usernames = request.POST.get('just_list_usernames', False)
            if just_list_usernames:
                return render_to_response(template_name, locals(), context_instance=RequestContext(request))
            else:
                has_error = handle_func(todo_list, group_name, level)
                is_finished = True
                return render_to_response(template_name, locals(), context_instance=RequestContext(request))
        else:
            return render_to_response(template_name, locals(), context_instance=RequestContext(request))
    else:
        form = BatchUserForm()
        return render_to_response(template_name, locals(), context_instance=RequestContext(request))

        
@user_passes_test(is_user_admin_logged_in, login_url = '/user-admin/login')
def add(request):
    return batch_user_handle(request, 'user_admin/add.html', util.add_users)

    
@user_passes_test(is_user_admin_logged_in, login_url = '/user-admin/login')
def remove(request):
    return batch_user_handle(request, 'user_admin/remove.html', util.remove_users)
    
    
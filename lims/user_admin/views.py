# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from lims.views import login_in_template, logout_in_template
    
def login(request):
    return login_in_template(request, 'UserAdmin', 'user_admin/login.html', '/user-admin')

def logout(request):
    return logout_in_template(request, '/user-admin/login')

def search(request):
    return render_to_response('user_admin/search.html');
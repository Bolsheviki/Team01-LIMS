# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from lims.views import login_in_template, search_in_template, logout_in_template
from lims.util import is_counter_admin_logged_in


def base(request):
    return render_to_response('counter_admin/base.html', { 'app': 'counter-admin' })
    
def borrow(request):
    return render_to_response('counter_admin/borrow.html', locals());
	
def return_(request):
    return render_to_response('counter_admin/return.html', locals());
	
def clear(request):
    return render_to_response('counter_admin/clear.html', locals());
	
def login(request):
	return login_in_template(request, 'CounterAdmin', 'counter_admin/login.html', '/counter-admin/')
	
@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/')
def logout(request):
    return logout_in_template(request, '/counter-admin/login/')	

	
@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/')
def search(request):
    return search_in_template(request, 'counter_admin/search.html', 'counter-admin');
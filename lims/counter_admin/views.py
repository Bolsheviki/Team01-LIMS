# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def test(request):
    return render_to_response('counter_admin/test.html', locals());
    
def borrow(request):
    return render_to_response('counter_admin/borrow.html', locals());
	
def return_(request):
    return render_to_response('counter_admin/return.html', locals());
	
def clear(request):
    return render_to_response('counter_admin/clear.html', locals());
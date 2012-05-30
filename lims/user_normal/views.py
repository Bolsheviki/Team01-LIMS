# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def test(request):
    return render_to_response('user/test.html', locals());
    

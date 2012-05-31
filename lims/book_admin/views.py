# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def test(request):
    return render_to_response('book_admin/test.html', locals());
    

def search(request):
    return render_to_response('book_admin/search.html', locals());


def add(request):
    return render_to_response('book_admin/add.html', locals());


def audit(request):
    return render_to_response('book_admin/audit.html', locals());


# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from lims.views import search_in_template

def test(request):
    return render_to_response('book_admin/test.html', locals());
    

def search(request):
    return search_in_template(request, 'book_admin/search.html');


def remove(request):
    return search_in_template(request, 'book_admin/remove.html');


def add(request):
    return render_to_response('book_admin/add.html', locals());


def audit(request):
    return render_to_response('book_admin/audit.html', locals());


# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from lims.views import search_in_template
from book_admin.forms import AddBookForm
from book_admin import util


def test(request):
    return render_to_response('book_admin/test.html', locals());
    

def search(request):
    return search_in_template(request, 'book_admin/search.html');


def remove(request):
    return render_to_response('book_admin/remove.html', locals());


def add(request):
    if 'isbn' in request.GET:
        form = AddBookForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data
            bookId = util.add_book(q['isbn'])
    else:
        form = AddBookForm()
    return render_to_response('book_admin/add.html', locals())


def audit(request):
    return render_to_response('book_admin/audit.html', locals());


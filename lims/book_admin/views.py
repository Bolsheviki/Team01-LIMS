# Create your views here.
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from lims.views import search_in_template, info_book_in_template, \
						login_in_template, logout_in_template
from book_admin.forms import AddBookForm, RemoveBookForm
from book_admin import util
from lims.util import is_book_admin_logged_in
from db.models import BookInstance


def base(request):
    return render_to_response('book_admin/base.html', { 'app': 'book-admin' })


def login(request):
	return login_in_template(request, 'BookAdmin', 'book_admin/login.html', '/book-admin/', is_book_admin_logged_in)


@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def logout(request):
    return logout_in_template(request, '/book-admin/login/')


@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def search(request):
    return search_in_template(request, 'book_admin/search.html', 'book-admin');


@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def remove(request):
    user = request.user
    if 'bookId' in request.GET:
        form = RemoveBookForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data
            bookId = q['bookId']
            BookInstance.objects.filter(id=bookId).update(removed=True)
    else:
        form = RemoveBookForm()
    return render_to_response('book_admin/remove.html', locals());


@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def add(request):
    user = request.user
    if 'isbn' in request.GET:
        form = AddBookForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data
            bookId = util.add_book(q['isbn'])
    else:
        form = AddBookForm()
    return render_to_response('book_admin/add.html', locals())


@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def audit(request):
    user = request.user
    return render_to_response('book_admin/audit.html', locals());

    
@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def info_book(request, isbn):
    user = request.user
    return info_book_in_template(request, isbn, 'book_admin/book.html')
	
	
	
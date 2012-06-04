# Create your views here.
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from lims.views import search_in_template, info_book_in_template, \
						login_in_template, logout_in_template, \
						settings_in_template
from book_admin.forms import AddBookForm, RemoveBookForm
from book_admin import util
from lims.util import is_book_admin_logged_in, get_borrows_each_month, get_top_borrows_in_month
from db.models import BookInstance, Book, Borrow


def base(request):
    return render_to_response('book_admin/base.html', { 'app': 'book-admin' })


def login(request):
	return login_in_template(request, 'BookAdmin', 'book_admin/login.html', '/book-admin/', is_book_admin_logged_in, 'book-admin')

	
def settings(request):
	return settings_in_template(request, 'book_admin/settings.html', 'book-admin')

	
@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def logout(request):
    return logout_in_template(request, '/book-admin/login/')


@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def search(request):
    return search_in_template(request, 'book_admin/search.html', 'book-admin');


@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def remove(request):
    app = 'book-admin'
    if 'bookId' in request.GET:
        form = RemoveBookForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data
            bookId = q['bookId']
            BookInstance.objects.filter(id=bookId).update(removed=True)
    else:
        form = RemoveBookForm()
    return render_to_response('book_admin/remove.html', locals(), context_instance=RequestContext(request));


@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def add(request):
    app = 'book-admin'
    if 'isbn' in request.GET:
        form = AddBookForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data
            bookId = util.add_book(q['isbn'])
    else:
        form = AddBookForm()
    return render_to_response('book_admin/add.html', locals(), context_instance=RequestContext(request))


@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def audit(request):
    app = 'book-admin'
    top_borrows = get_top_borrows_in_month()
    seq = 0
    for top in top_borrows:
        book = Book.objects.get(isbn=top['isbn'])
        top['book'] = book
        seq += 1
        top['seq'] = seq
    total_books = BookInstance.objects.filter(removed=False).count()
    total_borrowing_now = Borrow.objects.all().count()
    total_avaliable_now = total_books - total_borrowing_now
    borrow_statis = get_borrows_each_month()
    max = 0.5
    for statis in borrow_statis:
        if max < statis['borrow_times']:
            max = statis['borrow_times']
    step = int(round((max / 5 + 0.5)))
    max = step * 5
    for statis in borrow_statis:
        statis['borrow_times'] = statis['borrow_times'] * 100.0 / max
    divide = []
    i = 0
    while i <= max:
        divide.append(i)
        i += step
    return render_to_response('book_admin/audit.html', locals(), context_instance=RequestContext(request));


@user_passes_test(is_book_admin_logged_in, login_url = '/book-admin/login/')
def info_book(request, isbn):
    return info_book_in_template(request, isbn, 'book_admin/book.html', 'book-admin')
	
	
	
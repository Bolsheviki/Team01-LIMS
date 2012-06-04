# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from lims.views import login_in_template, search_in_template, logout_in_template
from lims.util import is_counter_admin_logged_in
from counter_admin.forms import DebtClearForm, BookBorrowForm, BookReturnForm
from django.contrib.auth.models import User, Group
from db.models import BookInstance
from db.models import Book
from db.models import UserProfile
from db.models import Record
from db.models import Borrow
from django.db.models import Q



def base(request):
    return render_to_response('counter_admin/base.html', { 'app': 'counter-admin' })

@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/')    
def borrow(request):
    user = request.user
    if 'bookId' in request.GET:
        form = BookBorrowForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data
            bookId = q['bookId']
            query = q['query']
            BookInstance.objects.filter(id=bookId).update(state='B')
			
            new_user = UserProfile.objects.get(user__username=query)
            new_book = BookInstance.objects.get(id=bookId)
			
            record = Record.objects.create(
				booki = new_book,
				user = new_user,
				action = 'B',
				time = 1,
			)
			
            instance = Borrow.objects.create(record = record)
			
    else:
        form = BookBorrowForm()
    return render_to_response('counter_admin/borrow.html', locals());

@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/') 	
def return_(request):
    user = request.user
    if 'bookId' in request.GET:
        form = BookReturnForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data
            bookId = q['bookId']
            BookInstance.objects.filter(id=bookId).update(state='U')
			
           # new_user = Borrow.objects.filter(record__booki=bookId)
            new_book = BookInstance.objects.get(id=bookId)
            new_user = Borrow.objects.get(record__booki__id=bookId).record.user
			#values('record').values('user')
           
           # new_user = UserProfile.objects.get(user__username=new_borrow__record__user__username)
            new_user = UserProfile.objects.get(user__username='dhuang')
            record = Record.objects.create(
				booki = new_book,
				user = new_user,
				action = 'R',
				time = "",
            )
    else:
        form = BookReturnForm()
    return render_to_response('counter_admin/return.html', locals());
	
@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/') 
def clear(request):
    user = request.user
    if request.method == 'POST':
        form = DebtClearForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data
            query = q['query']
            # #query = request.GET['query']
            UserProfile.objects.filter(user__username=query).update(debt=0)
            #BookInstance.objects.filter(id=query).update(removed=True)
    else:
		form =  DebtClearForm()
    #UserProfile.objects.filter(user=1).update(debt=0)
	
    return render_to_response('counter_admin/clear.html', locals());
	
def login(request):
	return login_in_template(request, 'CounterAdmin', 'counter_admin/login.html', '/counter-admin/', is_counter_admin_logged_in)
	
@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/')
def logout(request):
    return logout_in_template(request, '/counter-admin/login/')	

	
@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/')
def search(request):
    return search_in_template(request, 'counter_admin/search.html', 'counter-admin');
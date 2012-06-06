# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from lims.views import login_in_template, search_in_template, logout_in_template,  settings_in_template
from lims.util import is_counter_admin_logged_in
from django.template import RequestContext
from counter_admin.forms import DebtClearForm, BookBorrowForm, BookReturnForm
from django.contrib.auth.models import User, Group
from db.models import BookInstance, Book, UserProfile, Record, Borrow
from django.db.models import Q


def base(request):
    return render_to_response('counter_admin/base.html', { 'app': 'counter-admin' })
	

def settings(request):
    return settings_in_template(request, 'counter_admin/settings.html', 'counter-admin' )

    
@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/')    
def borrow(request):
    app = 'counter-admin'
    user = request.user
    if 'bookId' in request.GET:
        form = BookBorrowForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data
            bookId = q['bookId']
            query = q['query']
			
            new_book = BookInstance.objects.get(id=bookId)
            new_user = UserProfile.objects.get(user__username=query)
            record = Record.objects.create(
				booki = new_book,
				user = new_user,
				action = 'B',
			)
            current_time = record.time
            overtime_list = []
            borrow_books = Borrow.objects.filter(record__user=new_user)
            
            for aBook in borrow_books:
                borrow_time = aBook.record.time
                overtime_days = ( current_time - borrow_time ).days - 30
                if aBook.record.booki.renewal == True:
                    overtime_days = overtime_days - 30
                if overtime_days > 0:
                    booki = aBook.record.booki
                    overtime_list.append(booki)
                    
            if overtime_list:
                Record.objects.order_by('-time')[0].delete()
                return render_to_response('counter_admin/borrow.html', locals(), context_instance=RequestContext(request))
            
            BookInstance.objects.filter(id=bookId).update(state='B') 
            Borrow.objects.create(record = record)
    else:
        form = BookBorrowForm()
        bookId = -1
    return render_to_response('counter_admin/borrow.html', locals(), context_instance=RequestContext(request) );

    
@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/') 	
def return_(request):
    app = 'counter-admin'
    user = request.user
    if 'bookId' in request.GET:
        form = BookReturnForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data
            bookId = q['bookId']

            BookInstance.objects.filter(id=bookId).update(state='U')
            new_book = BookInstance.objects.get(id=bookId)
            new_user = Borrow.objects.get(record__booki__id=bookId).record.user
            borrow_time = Borrow.objects.get(record__booki__id=bookId).record.time
            record = Record.objects.create(
				booki = new_book,
				user = new_user,
				action = 'R',
            )
            Borrow.objects.get(record__booki__id=bookId).delete()
		    
            return_time = record.time
            overtime_days = (return_time-borrow_time).days - 30
            if new_book.renewal == True:
                overtime_days = overtime_days - 30
            if overtime_days > 0:
                debt = overtime_days
                new_user.debt += debt
                new_user.save() # here 'save' is update
    else:
        form = BookReturnForm()
        bookId = -1
    return render_to_response('counter_admin/return.html', locals(), context_instance=RequestContext(request));
	
    
@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/') 
def clear(request):
    app = 'counter-admin'
    user = request.user
    if request.method == 'POST':
        form = DebtClearForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data
            query = q['query']
            if request.POST.get('form-submit') == 'Clear':
                debt = UserProfile.objects.get(user__username=query).debt
                UserProfile.objects.filter(user__username=query).update(debt=0) 
                clear_correct = True
            if request.POST.get('form-submit') == 'View':
                view_correct = True
                debt = UserProfile.objects.get(user__username=query).debt
    else:
		form = DebtClearForm()
	
    return render_to_response('counter_admin/clear.html', locals(), context_instance=RequestContext(request));
	
    
def login(request):
	return login_in_template(request, 'CounterAdmin', 'counter_admin/login.html', '/counter-admin/', is_counter_admin_logged_in, 'counter-admin')
	
    
@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/')
def logout(request):
    return logout_in_template(request, '/counter-admin/login/')	

	
@user_passes_test(is_counter_admin_logged_in, login_url = '/counter-admin/login/')
def search(request):
    return search_in_template(request, 'counter_admin/search.html', 'counter-admin');

    
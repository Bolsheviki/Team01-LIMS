# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from normal_user import util
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from lims.views import settings_in_template, search_in_template, info_book_in_template, login_in_template, logout_in_template
from lims.util import is_normal_user_logged_in
from django.views.generic import list_detail
from db.models import BookInstance, Book, Borrow, Record
from django.db.models import Q


def base(request):
    return render_to_response('normal_user/base.html', { 'app': 'normal-user' })


def login(request):
    return login_in_template(request, 'NormalUser', 'normal_user/login.html', '/normal-user/', is_normal_user_logged_in)


def search(request):
    return search_in_template(request, 'normal_user/search.html', 'normal-user');


@user_passes_test(is_normal_user_logged_in, login_url = '/normal-user/login/')
def settings(request):
    return settings_in_template(request, 'normal_user/settings.html')
    

@user_passes_test(is_normal_user_logged_in, login_url = '/normal-user/login/')
def logout(request):
    return logout_in_template(request, '/normal-user/login/')


@user_passes_test(is_normal_user_logged_in, login_url = '/normal-user/login/')
def info_book(request, isbn):
    borrows = Borrow.objects.filter(Q(record__booki__book__isbn=isbn)&Q(record__action__exact='B'))
    return info_book_in_template(request, isbn, borrows, 'normal_user/book.html', 'normal-user')


@user_passes_test(is_normal_user_logged_in, login_url = '/normal-user/login/')
def information(request):
    app = 'normal-user'

    userprofile = util.getUser(request.user.username)
    username = request.user.username
    email = request.user.email
    level = userprofile.level[0]
    debt = userprofile.debt

    borrow_list = util.getBorrow_now(request.user.username)
    tlist = []
    for br in borrow_list:
        temp = {}
        temp['id'] = br.record.booki.id
        temp['isbn'] = br.record.booki.book.isbn
        temp['name'] = br.record.booki.book.title
        temp['time'] = br.record.time
        temp['renewal'] = br.record.booki.renewal
        tlist.append(temp)

    p = request.GET.get('page', '1')
    if not p.isdigit():
        p = 1
    else:
        p = int(p)

    relist = []
    paginator = Paginator(tlist , 1)

    try:
        relist = paginator.page(p)
    except:
        relist = paginator.page(1)
        
        
    return render_to_response('normal_user/information.html',
        {'app':app,
        'username':username,
        'email':email,
        'level':level,
        'debt':debt,
        'tlist':relist,
        'page_obj':relist,
        'is_paginated':True
        },
        context_instance=RequestContext(request)
    )

@user_passes_test(is_normal_user_logged_in, login_url = '/normal-user/login/')
def borrowbook(request):
    app = 'normal-user'
    borrow_list = util.getBorrow_now(request.user.username)
    tlist = []
    for br in borrow_list:
        temp = {}
        temp['id'] = br.record.booki.id
        temp['isbn'] = br.record.booki.book.isbn
        temp['name'] = br.record.booki.book.title
        temp['time'] = br.record.time
        temp['renewal'] = br.record.booki.renewal
        tlist.append(temp)

    p = request.GET.get('page', '1')
    if not p.isdigit():
        p = 1
    else:
        p = int(p)

    relist = []
    paginator = Paginator(tlist , 1)

    try:
        relist = paginator.page(p)
    except:
        relist = paginator.page(1)
        
    return render_to_response('normal_user/borrow.html', {'app':app,'tlist':relist, 'page_obj':relist, 'is_paginated':True}, context_instance=RequestContext(request))


@user_passes_test(is_normal_user_logged_in, login_url = '/normal-user/login/')
def allbook(request):
    app = 'normal-user'
    borrow_list = util.getBorrow_now(request.user.username)
    pre_list = util.getBorrow_retn(request.user.username)
    tlist = []
    for br in borrow_list:
        temp = {}
        temp['isbn'] = br.record.booki.book.isbn
        temp['name'] = br.record.booki.book.title
        temp['time'] = br.record.time
        temp['state'] = br.record.action[0]
        tlist.append(temp)
    for br in pre_list:
        temp = {}
        temp['isbn'] = br.record.booki.book.isbn
        temp['name'] = br.record.booki.book.title
        temp['time'] = br.record.time
        temp['state'] = br.record.action[0]
        tlist.append(temp)

    p = request.GET.get('page', '1')
    if not p.isdigit():
        p = 1
    else:
        p = int(p)

    relist = []
    paginator = Paginator(tlist , 1)
        
    try:
        relist = paginator.page(p)
    except:
        relist = paginator.page(1)
            
    return render_to_response('normal_user/allbook.html', {'app':app, 'tlist':relist, 'page_obj':relist, 'is_paginated':True}, context_instance=RequestContext(request))


@user_passes_test(is_normal_user_logged_in, login_url = '/normal-user/login/')
def renewal(request):
    sid = request.POST.get('id')
    util.setRenewal(request.user.username, sid)
    return HttpResponseRedirect('/normal-user/information/')


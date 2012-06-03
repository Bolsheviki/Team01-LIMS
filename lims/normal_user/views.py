# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from normal_user import util
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def test(request):
    return render_to_response('normal_user/test.html', locals());

def base(request):
    if request.user.is_authenticated():
        return render_to_response('normal_user/base.html', {'user':request.user})
    else:
        return render_to_response('login.html', {'error':False})

def information(request):
    if request.user.is_authenticated():
        userprofile = util.getUser(request.user.username)
        username = request.user.username
        email = request.user.email
        level = userprofile.level[0]
        debt = userprofile.debt
        
        return render_to_response('normal_user/information.html',
            {'username':username,
             'email':email,
             'level':level,
             'debt':debt
            }
        )
    else:
        return render_to_response('login.html', {'error':False})
        
def borrowbook(request):
    if request.user.is_authenticated():
        borrow_list = util.getBorrow_now(request.user.username)
        tlist = []
        for br in borrow_list:
            temp = {}
            temp['isbn'] = br.record.booki.book.isbn
            temp['name'] = br.record.booki.book.name
            temp['time'] = br.record.time
            temp['renewal'] = br.record.booki.renewal
            tlist.append(temp)

        relist = []
        paginator = Paginator(tlist , 1)
        
        page = request.GET.get('page')
        try:
            relist = paginator.page(page)
        except PageNotAnInteger:
            relist = paginator.page(1)
        except EmptyPage:
            relist = paginator.page(paginator.num_pages)
        except:
            relist = paginator.page(1)
            
        return render_to_response('normal_user/borrow.html', {'tlist':relist})
    else:
        return render_to_response('login.html', {'error':False})

def allbook(request):
    if request.user.is_authenticated():
        borrow_list = util.getBorrow_now(request.user.username)
        pre_list = util.getBorrow_retn(request.user.username)
        tlist = []
        for br in borrow_list:
            temp = {}
            temp['isbn'] = br.record.booki.book.isbn
            temp['name'] = br.record.booki.book.name
            temp['time'] = br.record.time
            temp['state'] = br.record.action[0]
            tlist.append(temp)
        for br in pre_list:
            temp = {}
            temp['isbn'] = br.record.booki.book.isbn
            temp['name'] = br.record.booki.book.name
            temp['time'] = br.record.time
            temp['state'] = br.record.action[0]
            tlist.append(temp)

        relist = []
        paginator = Paginator(tlist , 1)
        
        page = request.GET.get('page', '')
        try:
            relist = paginator.page(page)
        except PageNotAnInteger:
            relist = paginator.page(1)
        except EmptyPage:
            relist = paginator.page(paginator.num_pages)
        except:
            relist = paginator.page(1)
            
        return render_to_response('normal_user/allbook.html', {'tlist':relist})
    else:
        return render_to_response('login.html', {'error':False})

def renewal(request):
    if request.user.is_authenticated():
        isbn = request.POST.get('isbn')
        util.setRenewal(request.user.username, isbn)
        return HttpResponseRedirect('/normal-user/borrow/')
    else:
        return render_to_response('login.html', {'error':False})

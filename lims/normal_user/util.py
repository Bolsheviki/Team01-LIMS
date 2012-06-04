from db.models import Borrow, UserProfile, BookInstance

def getUser(name):
    users = UserProfile.objects.get(user__username__exact=name)
    return users

def setRenewal(name, sid):
    id = int(sid)
    try:
        br = Borrow.objects.get(record__user__user__username__exact=name, record__booki__id=id)
    except:
       print 'a'
    booki = br.record.booki
    booki.renewal = True
    booki.save()

def getBorrow_now(name):
    borrows = Borrow.objects.filter(record__user__user__username__exact=name, record__action__exact='B')
    return borrows

def getBorrow_retn(name):
    borrows = Borrow.objects.filter(record__user__user__username__exact=name, record__action__exact='R')
    return borrows

from db.models import Borrow, UserProfile, BookInstance

def getUser(name):
    users = UserProfile.objects.get(user__username__exact=name)
    return users

def setRenewal(name, isbns):
    isbn = int(isbns)
    try:
        br = Borrow.objects.get(user__user__username__exact=name, record__booki__book__isbn=isbn)
    except:
       return
    booki = br.record.booki
    booki.renewal = True
    booki.save()

def getBorrow_now(name):
    borrows = Borrow.objects.filter(user__user__username__exact=name, record__action__exact='B')
    return borrows

def getBorrow_retn(name):
    borrows = Borrow.objects.filter(user__user__username__exact=name, record__action__exact='R')
    return borrows

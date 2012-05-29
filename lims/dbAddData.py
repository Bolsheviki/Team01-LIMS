from records.models import Book, BookInstance, Record, Borrow, UserProfile
from django.contrib.auth.models import User
from django.db.models import Q

def create_test():
    Record.objects.all().delete()
    Borrow.objects.all().delete()
    BookInstance.objects.all().delete()
    Book.objects.all().delete()
#    UserProfile.objects().all().delete()
#    User.objects().exclude(username='root').delete()

    cccpA = Book.objects.create(isbn=1, name='cccp A', category=1, retrieval=1)
    cccpB = Book.objects.create(isbn=2, name='cccp B', category=2, retrieval=2)
    cccpi = BookInstance.objects.create(book=cccpA)
    cccpj = BookInstance.objects.create(book=cccpA)
    cccpk = BookInstance.objects.create(book=cccpB)
    try:
        dhuang = User.objects.create_user(username='dhuang', password='dhuang')
        dhuangi = UserProfile.objects.create(user=dhuang, level='U', debt=10)
    except:
        dhuangi = UserProfile.objects.get(user__username='dhuang')
        print 'redefine %s' % dhuangi
        
    r1 = Record.objects.create(booki=cccpi, user=dhuangi, action='B')
    r2 = Record.objects.create(booki=cccpj, user=dhuangi, action='B')
    Borrow.objects.create(user=dhuangi, record=r1)
    Borrow.objects.create(user=dhuangi, record=r2)
    Borrow.objects.get(
        Q(record__user=dhuangi) &
        Q(record__booki=cccpj)).delete()
    r3 = Record.objects.create(booki=cccpj, user=dhuangi, action='R')


def check_test():
    r = Record.objects.filter(user__user__username='dhuang')
    b = Borrow.objects.filter(user__user__username='dhuang')
#    b = Borrow.objects.all()
    u = User.objects.filter(username='dhuang')
    print u
    print r
    print b

create_test()
check_test()



from records.models import Book, BookInstance, Record, Borrow
from django.contrib.auth.models import User

def create_test():
    cccp = Book.objects.create(isbn=1, name='cccp')
    ussr = Book.objects.create(isbn=2, name='ussr')
    cccpi = BookInstance.objects.create(book=cccp)
    cccpi = BookInstance.objects.create(book=cccp)
    ussri = BookInstance.objects.create(book=ussr)
    dhuang = User.objects.create_user(
        username='b091220041', 
        email='bolsheviki@yeah.net',
        password='root')
    dhuang.last_name = 'dhuang'
    dhuang.save()
    r1 = Record.objects.create(booki=cccpi, user=dhuang, action='B')
    r2 = Record.objects.create(booki=ussri, user=dhuang, action='B')
    r3 = Record.objects.create(booki=ussri, user=dhuang, action='R')
    Borrow.objects.create(user=dhuang, record=r1)
    Borrow.objects.create(user=dhuang, record=r2)


def check_test():
    r = Record.objects.filter(user__last_name='dhuang')
    b = Borrow.objects.filter(user__last_name='dhuang')
    b = Borrow.objects.all()
    u = User.objects.filter(last_name='dhuang')
    print u
    print r
    print b

#create_test()
check_test()



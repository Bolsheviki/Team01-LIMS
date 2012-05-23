from records.models import Book, BookInstance, User, Record, Borrow

def create_test():
    cccp = Book.objects.create(isbn=1, name='cccp')
    ussr = Book.objects.create(isbn=2, name='ussr')
    cccpi = BookInstance.objects.create(book=cccp)
    cccpi = BookInstance.objects.create(book=cccp)
    ussri = BookInstance.objects.create(book=ussr)
    dhuang = User.objects.create(
        uid='b091220041', name='dhuang',
        email='bolsheviki@yeah.net',
        password='root')
    r1 = Record.objects.create(booki=cccpi, user=dhuang, action='B')
    r2 = Record.objects.create(booki=ussri, user=dhuang, action='B')
    r3 = Record.objects.create(booki=ussri, user=dhuang, action='R')
    Borrow.objects.create(user=dhuang, record=r1)
    Borrow.objects.create(user=dhuang, record=r2)


def check_test():
    r = Record.objects.filter(user__name='dhuang')
    b = Borrow.objects.filter(user__name='dhuang')
    b = Borrow.objects.all()
    print r
    print b


check_test()

# create_test()


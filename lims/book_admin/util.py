# Create your views here.
from db.models import Book, BookInstance, Record
from lims import util
from datetime import datetime, timedelta, date
from django.utils.timezone import utc
from django.utils import timezone
import calendar
from django.db.models import Q, Count
from django.db import connection, transaction


def add_book(isbn):
    try:
        book = Book.objects.get(isbn=isbn)
    except:
        book = ''
    if not book:
        bookInfo = util.info_book(isbn)
        if not bookInfo:
            return -1
        book = Book.objects.create(
            isbn=isbn,
            title=bookInfo.get('title', ''),
            authors=bookInfo.get('author', ''),
            translators=bookInfo.get('translator', ''),
            publisher=bookInfo.get('publisher', ''),
        )
    instance = BookInstance.objects.create(book=book)
    return instance.id

    
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

    
def get_top_borrows_in_month():
#    d = datetime.utcnow().replace(tzinfo=utc)
    d = timezone.now()
    print d
    if d.month == 1:
        year = 1
        month = 12
    else:
        year = d.year
        month = d.month - 1
    days = calendar.monthrange(year, month)[1]
    month_ago = d - timedelta(days=days)
    cursor = connection.cursor()
    cursor.execute('''
        select db_book.isbn, count(db_record.id) borrow_times
        from db_book, db_record, db_bookinstance
        where db_book.id = db_bookinstance.book_id and 
                db_record.booki_id = db_bookinstance.id and 
                db_record.action = 'B' and db_record.time >= %s
        group by db_book.isbn
        order by borrow_times desc
    ''', [ month_ago ])
    res = dictfetchall(cursor)
    cursor.close()
    return res
    

def get_borrows_each_month(isbn = 0):
    d = timezone.now()
#    d = datetime.utcnow().replace(tzinfo=utc)
    year = d.year - 1
    times = []
    for month in range(d.month + 1, 13):
        times.append(datetime(year, month, 1))
    year = d.year
    for month in range(1, d.month + 1):
        times.append(datetime(year, month, 1))
    times.append(d)
    cursor = connection.cursor()
    res = []
    max = 0
    for i in range(0, 12):
        if isbn == 0:
            cursor.execute('''
                select count(db_record.id) borrow_times
                from db_book, db_record, db_bookinstance
                where db_book.id = db_bookinstance.book_id and 
                        db_record.booki_id = db_bookinstance.id and 
                        db_record.action = 'B' and 
                        db_record.time >= %s and db_record.time < %s
                group by db_book.isbn
            ''', [ times[i], times[i + 1] ])
        else:
            cursor.execute('''
                select count(db_record.id) borrow_times
                from db_book, db_record, db_bookinstance
                where db_book.id = db_bookinstance.book_id and 
                        db_record.booki_id = db_bookinstance.id and 
                        db_record.action = 'B' and db_book.isbn = %s and
                        db_record.time >= %s and db_record.time < %s
                group by db_book.isbn
            ''', [ isbn, times[i], times[i + 1] ])
        res_in_month = dictfetchall(cursor)
        if not res_in_month:
            res_in_month.append({ 'borrow_times': 0 })
        res_in_month[0]['month'] = times[i].strftime('%b')
        res.append(res_in_month[0])
    cursor.close()
    return res

    
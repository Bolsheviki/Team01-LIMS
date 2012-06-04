from db.models import Book, BookInstance, Borrow, Record
import urllib2
from xml.dom import minidom
from django.db.models import Q
from datetime import datetime, timedelta, date
from django.utils.timezone import utc
from django.utils import timezone
import calendar
from django.db import connection, transaction


apikey = '002bdcc12fb16e8a008396438f144b9e'
isbnURL = 'http://api.douban.com/book/subject/isbn/'


def get_attrvalue(node, attrname):
    return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []


def info_book(isbn):
    book = {}
    try:
        res = urllib2.urlopen(isbnURL + isbn + '?apikey=' + apikey)
    except:
        return book
    xmldoc = minidom.parse(res)
    entry = xmldoc.documentElement
        
    nodes_summary = get_xmlnode(entry, 'summary')
    if nodes_summary:
        book['summary'] = get_nodevalue(nodes_summary[0])

    nodes_link = get_xmlnode(entry, 'link')
    for node in nodes_link:
        if get_attrvalue(node, 'rel') == 'image':
            book['image'] = get_attrvalue(node, 'href')
            break

    nodes_attribute = get_xmlnode(entry, 'db:attribute')
    for node in nodes_attribute:
        book[get_attrvalue(node, 'name')] = get_nodevalue(node)
    return book


def get_books(scope, query):
    if scope == 'A':
        books = Book.objects.filter(Q(authors__icontains=query)|Q(translators__icontains=query))
    elif scope == 'I':
        books = Book.objects.filter(isbn=query)
    else: # 'T'
        books = Book.objects.filter(title__icontains=query)
    return books

    
def get_book_info(isbn):
    book_info = info_book(isbn)
    remained = BookInstance.objects.filter(Q(book__isbn=isbn)&Q(state='U'))
    book_info['remained'] = remained.count()
    if 'author-intro' in book_info.keys():
        book_info['author_intro'] = book_info['author-intro']
        del book_info['author-intro']
    return book_info
	

def is_in_group(user, group_name):
    return user.groups.filter(name = group_name).count() > 0

def is_normal_user_logged_in(user):
    return user.is_authenticated() and is_in_group(user, 'NormalUser')

def is_book_admin_logged_in(user):
    return user.is_authenticated() and is_in_group(user, 'BookAdmin')

def is_counter_admin_logged_in(user):
    return user.is_authenticated() and is_in_group(user, 'CounterAdmin')

def is_user_admin_logged_in(user):
    return user.is_authenticated() and is_in_group(user, 'UserAdmin')

  
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

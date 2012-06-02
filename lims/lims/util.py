from db.models import Book, BookInstance, Borrow, Record
import urllib2
from xml.dom import minidom
from django.db.models import Q


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
    books = BookInstance.objects.filter(Q(book__isbn=isbn)&Q(removed=False))
    records = Record.objects.filter(booki=books)
    print records
    borrow = records.filter(id__range=Borrow.objects.values_list('record', flat=True))
    print borrow
    remained = books.exclude(id__range=borrow.values_list('booki', flat=True))
    book_info['remained'] = remained.count()
    if 'author-intro' in book_info.keys():
        book_info['author_intro'] = book_info['author-intro']
        del book_info['author-intro']
    return book_info


def is_in_group(user, group_name):
    return user.groups.filter(name = group_name).count() > 0

def is_normal_user_logged_in(user):
    return user.is_authenticated() and is_in_group(user, 'NormalUser')

from db.models import Book
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
    if scope == 'T':
        books = Book.objects.filter(title__icontains=query)
    elif scope == 'A':
        books = Book.objects.filter(Q(authors__icontains=query)|Q(translators__icontains=query))
    elif scope == 'I':
        books = Book.objects.filter(isbn=query)
    else:
        books = Book.objects.filter(name__icontains='')
    return books


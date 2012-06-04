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
    borrows = Borrow.objects.filter(
                Q(record__booki__book__isbn=isbn)&
                Q(record__booki__removed=False))
    book_info['remained'] = books.count() - borrows.count()
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

#@login_required(login_url = '/login/')
#def loggedin(request):
#    return render_to_response('loggedin.html', {'user':request.user})

#@user_passes_test(is_normal_user_logged_in, login_url = '/login')
#def need_normal_user_logged_in(request):
#    return render_to_response('user_passes_test.html')

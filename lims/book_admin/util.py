# Create your views here.
from db.models import Book, BookInstance
from lims import util


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
        
#print add_book('9787111298854')

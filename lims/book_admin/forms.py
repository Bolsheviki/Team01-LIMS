from django import forms
from lims import util
from db.models import BookInstance
from django.db.models import Q
import re


def validate_book_isbn(isbn):
    book = util.info_book(isbn)
    if not book:
        raise forms.ValidationError(u'ISBN error')


class AddBookForm(forms.Form):
    isbn = forms.CharField(validators=[validate_book_isbn])

    
def validate_book_id(id):
    try:
        book = BookInstance.objects.get(Q(id=id)&Q(removed=False))
    except:
        raise forms.ValidationError(u'Book ID error')
    
class RemoveBookForm(forms.Form):
    bookId = forms.CharField(validators=[validate_book_id])
from django import forms
from lims import util
import re



def validate_book_isbn(isbn):
    book = util.info_book(isbn)
    if not book:
        raise forms.ValidationError(u'ISBN error')


class AddBookForm(forms.Form):
    isbn = forms.CharField(validators=[validate_book_isbn])

    

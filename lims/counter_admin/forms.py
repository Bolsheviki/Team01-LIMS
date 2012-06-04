from django import forms
from lims import util
from db.models import BookInstance
from db.models import Book
from db.models import Record
from db.models import Borrow
from db.models import UserProfile
from django.db.models import Q
import re
    
class DebtClearForm(forms.Form):
    query = forms.CharField()
   
    def clean_query(self):
        query = self.cleaned_data['query']
        try:
	        new_user = UserProfile.objects.get( Q(user__username=query) )
        except UserProfile.DoesNotExist:
            raise forms.ValidationError('The User is not exist')
        return query
   
class BookBorrowForm(forms.Form):
    query = forms.CharField()
    bookId = forms.CharField()

    def clean_query(self):
        query = self.cleaned_data['query']
        try:
	        new_user = UserProfile.objects.get( user__username=query )
        except UserProfile.DoesNotExist:
            raise forms.ValidationError('The User is not existed')
		
        debt = new_user.debt
        if debt > 0:
            raise forms.ValidationError('Debt should be cleared!')

        return query
		
    def clean_bookId(self):
        bookId = self.cleaned_data['bookId']
        try:
            new_book = BookInstance.objects.get(Q(id=bookId)&Q(state='U'))
        except BookInstance.DoesNotExist:
		    raise forms.ValidationError('The Book cannot be borrowed')
        return bookId
		
	

class BookReturnForm(forms.Form):
    bookId = forms.CharField()
    def clean_bookId(self):
        bookId = self.cleaned_data['bookId']
        try:
            new_user = Borrow.objects.get(record__booki__id=bookId)
        except Borrow.DoesNotExist:
		    raise forms.ValidationError('The Book is not in Borrow')
        return bookId
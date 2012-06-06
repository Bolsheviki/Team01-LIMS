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
            raise forms.ValidationError('该用户不存在')
        return query
   
   
class BookBorrowForm(forms.Form):
    query = forms.CharField()
    bookId = forms.CharField()

    def clean_query(self):
        query = self.cleaned_data['query']
        try:
	        new_user = UserProfile.objects.get(user__username=query)
        except UserProfile.DoesNotExist:
            raise forms.ValidationError('该用户不存在')
		
        debt = new_user.debt
        if debt > 0:
            raise forms.ValidationError('请该用户首先把欠款清除!')
        try:
            count = Borrow.objects.filter(record__user__user__username=query).count()
        except Borrow.DoesNotExist:
		    count = 0
		
        if new_user.level == 'U' and count > 5:		
		    raise forms.ValidationError('该用户已达借书限额，不能借更多的书')
        if new_user.level == 'G' and count > 7:		
		    raise forms.ValidationError('该用户已达借书限额，不能借更多的书')
        if new_user.level == 'S' and count > 9:		
		    raise forms.ValidationError('该用户已达借书限额，不能借更多的书')
        return query
		
    def clean_bookId(self):
        bookId = self.cleaned_data['bookId']
        try:
            new_book = BookInstance.objects.get(Q(id=bookId)&Q(state='U'))
        except BookInstance.DoesNotExist:
		    raise forms.ValidationError('这本书无法出借')
        return bookId
		
	
class BookReturnForm(forms.Form):
    bookId = forms.CharField()
    def clean_bookId(self):
        bookId = self.cleaned_data['bookId']
        try:
            new_user = Borrow.objects.get(record__booki__id=bookId)
        except Borrow.DoesNotExist:
		    raise forms.ValidationError('这本书没有被借过')
        return bookId
        
        
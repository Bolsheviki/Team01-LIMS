# -*- coding: cp936 -*-
from django import forms
from db import models
from lims.forms import SettingsForm
import string
from django.contrib.auth.models import User

USER_ADMIN_GROUP_CHOICES = (
    ('N', 'NormalUser'),
    ('B', 'BookAdmin'),
    ('C', 'CounterAdmin'),
)

class SearchForm(forms.Form):
    query = forms.CharField(required=False)
    scope = forms.ChoiceField(widget=forms.Select, choices=USER_ADMIN_GROUP_CHOICES)

class UserInfoForm(SettingsForm):
    level = forms.ChoiceField(required=False, widget=forms.Select, choices=models.LEVEL_CHOICES)
    debt = forms.IntegerField(required=False)

    def clean_debt(self):
        debt = self.cleaned_data['debt']
        if int(debt) < 0:
            raise forms.ValidationError('Debt should not be negative!')
        return debt

class BatchUserForm(forms.Form):
    batch_username = forms.CharField()
    from_index = forms.IntegerField()
    to_index = forms.IntegerField()
    wildcard_length = forms.IntegerField()
    group = forms.ChoiceField(widget=forms.Select, choices=USER_ADMIN_GROUP_CHOICES)
    level = forms.ChoiceField(widget=forms.Select, choices=models.LEVEL_CHOICES)
    just_list_usernames = forms.BooleanField(required=False, initial=True)

    def clean_batch_username(self):
        batch_username = self.cleaned_data['batch_username']
        if string.find(batch_username, r'(*)') == -1:
            raise forms.ValidationError('Wildcard not found!')
        return batch_username

    def clean_from_index(self):
        from_index = self.cleaned_data['from_index']
        if from_index < 0:
            raise forms.ValidationError('Index should not be negative!')

        return from_index

    def clean_to_index(self):
        to_index = self.cleaned_data['to_index']
        if to_index < 0:
            raise forms.ValidationError('Index should not be negative!')

        try:
            from_index = self.cleaned_data['from_index']
        except:
            return to_index

        if from_index > to_index:
            raise forms.ValidationError('To-index should not be less than from-index!')

        return to_index
    
    def clean_wildcard_length(self):
        wildcard_length = self.cleaned_data['wildcard_length']

        try:
            to_index = self.cleaned_data['to_index']
        except:
            return wildcard_length

        if len(str(to_index)) > int(wildcard_length):
            raise forms.ValidationError('Wildcard length is not big enough!')
        return wildcard_length

class AddUserForm(forms.Form):
    username = forms.CharField()
    password_first = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    group = forms.ChoiceField(widget=forms.Select, choices=USER_ADMIN_GROUP_CHOICES)
    level = forms.ChoiceField(required=False, widget=forms.Select, choices=models.LEVEL_CHOICES)
    debt = forms.IntegerField(initial='0')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(u'用户名已存在！')
        return username

    def clean_password_first(self):
        pw_first = self.cleaned_data['password_first']
        need_reset_pw = self.cleaned_data.get('need_reset_password', False)
        if need_reset_pw and pw_first == '':
            raise forms.ValidationError('Password should not be empty!')
        return pw_first

    def clean_password_confirm(self):
        pw_confirm = self.cleaned_data['password_confirm']
        try:
            pw_first = self.cleaned_data['password_first']
        except:
            return pw_confirm

        if pw_first != pw_confirm:
            raise forms.ValidationError('Two inputs of password are not the same!')
        return pw_confirm
    
    def clean_debt(self):
        debt = self.cleaned_data['debt']
        if int(debt) < 0:
            raise forms.ValidationError('Debt should not be negative!')
        return debt

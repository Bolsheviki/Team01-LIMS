# -*- coding: cp936 -*-
from django import forms
from lims import util
from django.contrib.auth.models import User
from django.contrib import auth

QUERY_SCOPE_CHOICES = (
    ('T', 'Title'),
    ('A', 'Author'),
    ('I', 'ISBN'),
)

class SearchForm(forms.Form):
    query = forms.CharField(required=False)
    scope = forms.ChoiceField(widget=forms.Select, choices=QUERY_SCOPE_CHOICES)

class LoginForm(forms.Form):
    group_name = forms.CharField(widget=forms.HiddenInput)
    username = forms.CharField(label=u'�û���')
    password = forms.CharField(label=u'����', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            group_name = self.cleaned_data['group_name']
        except:
            return username
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(u'�û�������!')

        if not util.is_in_group(user, group_name):
            raise forms.ValidationError(u'���û�����%s�ĳ�Ա!' % (group_name))
        return username
    
    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            username = self.cleaned_data['username']
        except:
            return password
        
        user = auth.authenticate(username = username, password = password)
        if user is None or not user.is_active:
            raise forms.ValidationError(u'���벻��ȷ��')
        return password

class SettingsForm(forms.Form):
    need_reset_password = forms.BooleanField(label=u'�Ƿ���Ҫ�޸�����', initial=False, required=False)
    password_first = forms.CharField(label=u'����������', widget=forms.PasswordInput, required=False)
    password_confirm = forms.CharField(label=u'ȷ��������', widget=forms.PasswordInput, required=False)
    email = forms.EmailField(label=u'Email��ַ', required=False)
    first_name = forms.CharField(label=u'��', required=False)
    last_name = forms.CharField(label=u'��', required=False)

    def clean_password_first(self):
        pw_first = self.cleaned_data['password_first']
        need_reset_pw = self.cleaned_data.get('need_reset_password', False)
        if need_reset_pw and pw_first == '':
            raise forms.ValidationError(u'���벻��Ϊ�գ�')
        return pw_first

    def clean_password_confirm(self):
        pw_confirm = self.cleaned_data['password_confirm']
        try:
            pw_first = self.cleaned_data['password_first']
        except:
            return pw_confirm

        need_reset_pw = self.cleaned_data.get('need_reset_password', False)
        if need_reset_pw and pw_first != pw_confirm:
            raise forms.ValidationError(u'������������벻��ͬ��')
        return pw_confirm

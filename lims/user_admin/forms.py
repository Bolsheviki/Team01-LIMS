# -*- coding: cp936 -*-
from django import forms
from db import models
from lims.forms import SettingsForm
import string
from django.contrib.auth.models import User

USER_ADMIN_GROUP_CHOICES = (
    ('N', u'��ͨ�û�'),
    ('B', u'�鼮����Ա'),
    ('C', u'��̨����Ա'),
)

class SearchForm(forms.Form):
    query = forms.CharField(required=False)
    scope = forms.ChoiceField(widget=forms.Select, choices=USER_ADMIN_GROUP_CHOICES)

class UserInfoForm(SettingsForm):
    level = forms.ChoiceField(label=u'�û��ȼ�', required=False, widget=forms.Select, choices=models.LEVEL_CHOICES)
    debt = forms.IntegerField(label=u'Ƿ��', required=False)

    def clean_debt(self):
        debt = self.cleaned_data['debt']
        if int(debt) < 0:
            raise forms.ValidationError(u'Ƿ�����ֲ�ӦΪ����')
        return debt

class BatchUserForm(forms.Form):
    batch_username = forms.CharField(label=u'�û��������ַ���')
    from_index = forms.IntegerField(label=u'��ʼ����')
    to_index = forms.IntegerField(label=u'��ֹ����')
    wildcard_length = forms.IntegerField(label=u'ͨ�������')
    group = forms.ChoiceField(label=u'�û���', widget=forms.Select, choices=USER_ADMIN_GROUP_CHOICES)
    level = forms.ChoiceField(label=u'�û��ȼ�', widget=forms.Select, choices=models.LEVEL_CHOICES)
    just_list_usernames = forms.BooleanField(label=u'ֻ���г��û������ݲ�ִ�У�', required=False, initial=True)

    def clean_batch_username(self):
        batch_username = self.cleaned_data['batch_username']
        if string.find(batch_username, r'(*)') == -1:
            raise forms.ValidationError(u'δ�ҵ�ͨ���(*)!')
        return batch_username

    def clean_from_index(self):
        from_index = self.cleaned_data['from_index']
        if from_index < 0:
            raise forms.ValidationError(u'��ʼ���ֲ�ӦΪ����')

        return from_index

    def clean_to_index(self):
        to_index = self.cleaned_data['to_index']
        if to_index < 0:
            raise forms.ValidationError(u'��ֹ���ֲ�ӦΪ����')

        try:
            from_index = self.cleaned_data['from_index']
        except:
            return to_index

        if from_index > to_index:
            raise forms.ValidationError(u'��ʼ���ֲ�ӦС����ֹ���֣�')

        return to_index
    
    def clean_wildcard_length(self):
        wildcard_length = self.cleaned_data['wildcard_length']

        try:
            to_index = self.cleaned_data['to_index']
        except:
            return wildcard_length

        if len(str(to_index)) > int(wildcard_length):
            raise forms.ValidationError(u'ͨ������Ȳ��㣡')
        return wildcard_length

class AddUserForm(forms.Form):
    username = forms.CharField(label=u'�û���')
    password_first = forms.CharField(label=u'��������', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=u'ȷ������', widget=forms.PasswordInput)
    email = forms.EmailField(label=u'Email��ַ', required=False)
    first_name = forms.CharField(label=u'��', required=False)
    last_name = forms.CharField(label=u'��', required=False)
    group = forms.ChoiceField(label=u'�û���', widget=forms.Select, choices=USER_ADMIN_GROUP_CHOICES)
    level = forms.ChoiceField(label=u'�û��ȼ�', required=False, widget=forms.Select, choices=models.LEVEL_CHOICES)
    debt = forms.IntegerField(label=u'Ƿ��', initial='0')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(u'�û����Ѵ��ڣ�')
        return username

    def clean_password_first(self):
        pw_first = self.cleaned_data['password_first']
        need_reset_pw = self.cleaned_data.get('need_reset_password', False)
        if need_reset_pw and pw_first == '':
            raise forms.ValidationError(u'���벻ӦΪ�գ�')
        return pw_first

    def clean_password_confirm(self):
        pw_confirm = self.cleaned_data['password_confirm']
        try:
            pw_first = self.cleaned_data['password_first']
        except:
            return pw_confirm

        if pw_first != pw_confirm:
            raise forms.ValidationError(u'�����������벻ͬ��')
        return pw_confirm
    
    def clean_debt(self):
        debt = self.cleaned_data['debt']
        if int(debt) < 0:
            raise forms.ValidationError(u'Ƿ����ֵ��ӦΪ����')
        return debt

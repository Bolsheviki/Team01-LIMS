from django import forms
from db import models
from lims.forms import SettingsForm
import string
from django.contrib.auth.models import User

USER_ADMIN_GROUP_CHOICES = (
    ('N', u'普通用户'),
    ('B', u'书籍管理员'),
    ('C', u'柜台管理员'),
)

class SearchForm(forms.Form):
    query = forms.CharField(required=False)
    scope = forms.ChoiceField(widget=forms.Select, choices=USER_ADMIN_GROUP_CHOICES)

class UserInfoForm(SettingsForm):
    level = forms.ChoiceField(label=u'用户等级', required=False, widget=forms.Select, choices=models.LEVEL_CHOICES)
    debt = forms.IntegerField(label=u'欠款', required=False)

    def clean_debt(self):
        debt = self.cleaned_data['debt']
        if int(debt) < 0:
            raise forms.ValidationError(u'欠款数字不应为负！')
        return debt

class BatchUserForm(forms.Form):
    batch_username = forms.CharField(label=u'用户名描述字符串')
    from_index = forms.IntegerField(label=u'起始数字')
    to_index = forms.IntegerField(label=u'终止数字')
    wildcard_length = forms.IntegerField(label=u'通配符长度')
    group = forms.ChoiceField(label=u'用户组', widget=forms.Select, choices=USER_ADMIN_GROUP_CHOICES)
    level = forms.ChoiceField(label=u'用户等级', widget=forms.Select, choices=models.LEVEL_CHOICES)
    just_list_usernames = forms.BooleanField(label=u'只是列出用户名（暂不执行）', required=False, initial=True)

    def clean_batch_username(self):
        batch_username = self.cleaned_data['batch_username']
        if string.find(batch_username, r'(*)') == -1:
            raise forms.ValidationError(u'未找到通配符(*)!')
        return batch_username

    def clean_from_index(self):
        from_index = self.cleaned_data['from_index']
        if from_index < 0:
            raise forms.ValidationError(u'起始数字不应为负！')

        return from_index

    def clean_to_index(self):
        to_index = self.cleaned_data['to_index']
        if to_index < 0:
            raise forms.ValidationError(u'终止数字不应为负！')

        try:
            from_index = self.cleaned_data['from_index']
        except:
            return to_index

        if from_index > to_index:
            raise forms.ValidationError(u'起始数字不应小于终止数字！')

        return to_index
    
    def clean_wildcard_length(self):
        wildcard_length = self.cleaned_data['wildcard_length']

        try:
            to_index = self.cleaned_data['to_index']
        except:
            return wildcard_length

        if len(str(to_index)) > int(wildcard_length):
            raise forms.ValidationError(u'通配符长度不足！')
        return wildcard_length

class AddUserForm(forms.Form):
    username = forms.CharField(label=u'用户名')
    password_first = forms.CharField(label=u'输入密码', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=u'确认密码', widget=forms.PasswordInput)
    email = forms.EmailField(label=u'Email地址', required=False)
    first_name = forms.CharField(label=u'姓', required=False)
    last_name = forms.CharField(label=u'名', required=False)
    group = forms.ChoiceField(label=u'用户组', widget=forms.Select, choices=USER_ADMIN_GROUP_CHOICES)
    level = forms.ChoiceField(label=u'用户等级', required=False, widget=forms.Select, choices=models.LEVEL_CHOICES)
    debt = forms.IntegerField(label=u'欠款', initial='0')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(u'用户名已存在！')
        return username

    def clean_password_first(self):
        pw_first = self.cleaned_data['password_first']
        need_reset_pw = self.cleaned_data.get('need_reset_password', False)
        if need_reset_pw and pw_first == '':
            raise forms.ValidationError(u'密码不应为空！')
        return pw_first

    def clean_password_confirm(self):
        pw_confirm = self.cleaned_data['password_confirm']
        try:
            pw_first = self.cleaned_data['password_first']
        except:
            return pw_confirm

        if pw_first != pw_confirm:
            raise forms.ValidationError(u'两次密码输入不同！')
        return pw_confirm
    
    def clean_debt(self):
        debt = self.cleaned_data['debt']
        if int(debt) < 0:
            raise forms.ValidationError(u'欠款数值不应为负！')
        return debt

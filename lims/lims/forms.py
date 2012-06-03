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
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            group_name = self.cleaned_data['group_name']
        except:
            return username
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('User not exist!')

        if not util.is_in_group(user, group_name):
            raise forms.ValidationError('User not belong to group %s!' % (group_name))
        return username
    
    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            username = self.cleaned_data['username']
        except:
            return password
        
        user = auth.authenticate(username = username, password = password)
        if user is None or not user.is_active:
            raise forms.ValidationError('Password not matched!')
        return password

class SettingsForm(forms.Form):
    need_reset_password = forms.BooleanField(initial=False, required=False)
    password_first = forms.CharField(widget=forms.PasswordInput, required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=False)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

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

        need_reset_pw = self.cleaned_data.get('need_reset_password', False)
        if need_reset_pw and pw_first != pw_confirm:
            raise forms.ValidationError('Two inputs of password are not the same!')
        return pw_confirm

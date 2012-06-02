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
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    group_name = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        group_name = cleaned_data.get('group_name')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('User not exist!')

        if not util.is_in_group(user, group_name):
            raise forms.ValidationError('User not belong to group %s!' % (group_name))
        
        user = auth.authenticate(username = username, password = password)
        if user is None or not user.is_active:
            raise forms.ValidationError('Password not matched!')

        return cleaned_data
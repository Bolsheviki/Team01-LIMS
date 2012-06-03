from django import forms
from db import models

QUERY_SCOPE_CHOICES = (
    ('N', 'NormalUser'),
    ('B', 'BookAdmin'),
    ('C', 'CounterAdmin'),
)

class SearchForm(forms.Form):
    query = forms.CharField(required=False)
    scope = forms.ChoiceField(widget=forms.Select, choices=QUERY_SCOPE_CHOICES)

class UserInfoForm(forms.Form):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    level = forms.ChoiceField(required=False, widget=forms.Select, choices=models.LEVEL_CHOICES)
    debt = forms.IntegerField(required=False)

    def clean_debt(self):
        debt = self.cleaned_data['debt']
        if debt < 0:
            raise forms.ValidationError('Debt should not be negative!')
        return debt
                                
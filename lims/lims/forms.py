from django import forms


QUERY_SCOPE_CHOICES = (
    ('T', 'Title'),
    ('A', 'Author'),
    ('I', 'ISBN'),
)


class SearchForm(forms.Form):
    query = forms.CharField()
    scope = forms.ChoiceField(widget=forms.Select, choices=QUERY_SCOPE_CHOICES)

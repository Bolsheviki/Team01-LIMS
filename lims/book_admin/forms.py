from django import forms



class AddForm(forms.Form):
    isbn = forms.CharField()
    name = forms.CharField(required=False)
    category = forms.CharField(required=False)
    retrieval = forms.CharField(required=False)
    publisher = forms.CharField(required=False)
    authors = forms.CharField(required=False)
    abstract = forms.CharField(required=False)

    

from django import forms
from .models import Publisher


class PublisherForm(forms.ModelForm):
    '''
    A form that can be accessed by editors to create publishers.
    '''
    class Meta:
        model = Publisher
        fields = ("name", "description", "editors", "journalists")
        widgets = {
            'editors': forms.CheckboxSelectMultiple(),
            'journalists': forms.CheckboxSelectMultiple(),
        }

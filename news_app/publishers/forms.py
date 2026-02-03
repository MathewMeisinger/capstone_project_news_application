from django import forms
from .models import Publisher


class PublisherForm(forms.ModelForm):
    ''' A form that can be accessed by editors to create publishers.

        :model: Publisher
        :fields: The fields to be included in the form
        :widgets: Custom widgets for the form field allowing multiple
            selections
    '''
    class Meta:
        model = Publisher
        fields = ("name", "description", "editors", "journalists")
        widgets = {
            'editors': forms.CheckboxSelectMultiple(),
            'journalists': forms.CheckboxSelectMultiple(),
        }

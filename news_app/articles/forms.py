from django import forms
from .models import Article
from publishers.models import Publisher


class ArticleCreationForm(forms.ModelForm):
    '''
    Form for creating a new Article.
    Includes fields for title, content, and publisher.
    '''
    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if not self.user:
            self.fields['publisher'].queryset = Publisher.objects.none()
            return

        if self.user.role == 'journalist':
            self.fields['publisher'].queryset = Publisher.objects.filter(
                journalists=self.user
            )
        elif self.user.role == 'editor':
            self.fields['publisher'].queryset = Publisher.objects.filter(
                editors=self.user
            )

    def clean_publisher(self):
        publisher = self.cleaned_data.get('publisher')

        if not publisher:
            return publisher

        if self.user.role == 'journalist':
            if not publisher.journalists.filter(id=self.user.id).exists():
                raise forms.ValidationError(
                    "You are not a member of the selected Publisher"
                )

        return publisher

from django import forms
from .models import Newsletter
from articles.models import Article


class NewsletterForm(forms.ModelForm):
    '''
    Form for adding articles to newsletters
    '''
    class Meta:
        model = Newsletter
        fields = ('title', 'description', 'articles')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if not self.user:
            self.fields['articles'].queryset = Article.objects.none()
            return
        # journalists can only add their own approved articles
        if self.user.role == 'journalist':
            self.fields['articles'].queryset = Article.objects.filter(
                author=self.user,
                approved=True
            )
        # editors can add any approved articles
        elif self.user.role == 'editor':
            self.fields['articles'].queryset = Article.objects.filter(
                approved=True
            )

from django.contrib.auth.mixins import UserPassesTestMixin


class JournalistRequiredMixin(UserPassesTestMixin):
    '''
    Mixin to ensure that the user is a journalist.
    Journalists are users with is_journalist attribute set to True.
    '''
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == 'journalist'
        )


class EditorRequiredMixin(UserPassesTestMixin):
    '''
    Mixin to ensure that the user is an editor.
    Editors are users with is_editor attribute set to True.
    '''
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == 'editor'
        )


class ReaderRequiredMixin(UserPassesTestMixin):
    '''
    Mixin to ensure that the user is a reader.
    Readers are users with is_reader attribute set to True.
    '''
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == 'reader'
        )

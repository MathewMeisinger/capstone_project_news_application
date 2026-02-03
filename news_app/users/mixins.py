from django.contrib.auth.mixins import UserPassesTestMixin


class JournalistRequiredMixin(UserPassesTestMixin):
    ''' Mixin to ensure that the user is a journalist.

        :test_func: Checks if the user is authenticated and has the journalist
        role.
    '''
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == 'journalist'
        )


class EditorRequiredMixin(UserPassesTestMixin):
    ''' Mixin to ensure that the user is an editor.

        :test_func: Checks if the user is authenticated and has the editor
        role.
    '''
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == 'editor'
        )


class ReaderRequiredMixin(UserPassesTestMixin):
    ''' Mixin to ensure that the user is a reader.

        :test_func: Checks if the user is authenticated and has the reader
        role.
    '''
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == 'reader'
        )

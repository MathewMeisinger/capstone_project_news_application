from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    '''
    Create user roles and assign permissions.
    - reader: can view articles
    - editor: can view and edit articles
    - journalist: can view, edit, and create articles
    '''
    reader, _ = Group.objects.get_or_create(name='Reader')
    editor, _ = Group.objects.get_or_create(name='Editor')
    journalist, _ = Group.objects.get_or_create(name='Journalist')

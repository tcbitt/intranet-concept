from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Set up default user roles'

    def handle(self, *args, **kwargs):
        roles = ['Employee', 'Support', 'Admin']
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created role: {role}'))
            else:
                self.stdout.write(f'Role already exists: {role}')

'''
Run this command using:

python manage.py setup_roles
'''
# management/commands/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create student and teacher groups'

    def handle(self, *args, **options):
        student_group, created = Group.objects.get_or_create(name='Students')
        teacher_group, created = Group.objects.get_or_create(name='Teachers')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created student and teacher groups'))
        else:
            self.stdout.write(self.style.WARNING('Student and teacher groups already exist'))

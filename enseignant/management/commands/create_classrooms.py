# management/commands/create_groups_classrooms.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create DUT1 and DUT2 groups'

    def handle(self, *args, **options):
        DUT1_group, created = Group.objects.get_or_create(name='DUT1')
        DUT2_group, created = Group.objects.get_or_create(name='DUT2')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created DUT1 and DUT2 groups'))
        else:
            self.stdout.write(self.style.WARNING('DUT1 and DUT2 groups already exist'))

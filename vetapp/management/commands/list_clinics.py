from django.core.management.base import BaseCommand
from vetapp.models import Clinic


class Command(BaseCommand):
    help = 'Displays a list of all clinics'

    def handle(self, *args, **kwargs):
        clinics = Clinic.objects.all()
        self.stdout.write("List of clinics:")
        for clinic in clinics:
            self.stdout.write(clinic.name)

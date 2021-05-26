from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os
from django.conf import settings
from dotenv import load_dotenv

env_path = os.path.join(settings.BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not (User.objects.all().exists() and
                User.objects.filter(username=os.environ.get('DJANGO_SU_NAME')).exists()):
            print('Creating superuser admin account')
            User.objects.create_superuser(email=os.environ.get('DJANGO_SU_EMAIL'),
                                          username=os.environ.get('DJANGO_SU_NAME'),
                                          password=os.environ.get('DJANGO_SU_PASSWORD'))
        else:
            print("Admin already exists")

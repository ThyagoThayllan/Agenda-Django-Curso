import django
import os
import sys
from pathlib import Path


DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS_TO_CREATE = 250

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

django.setup()

from contact.models import Category
from contact.models import Contact
from faker import Faker
from random import choice


categories = list(Category.objects.all())

if not categories:
    raise Exception('Nenhuma categoria encontrada. Crie categories antes de executar o script.')

fake = Faker('pt_BR')

for _ in range(NUMBER_OF_OBJECTS_TO_CREATE):
    Contact.objects.create(
        category=choice(categories),
        description=fake.paragraph(),
        email=fake.email(),
        first_name=fake.name(),
        last_name=fake.last_name(),
        phone=fake.phone_number(),
        show=fake.boolean(),
    )

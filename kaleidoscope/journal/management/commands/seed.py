from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware
from datetime import timedelta, datetime

from journal.models import User, Entry

import pytz
from faker import Faker
from random import randint, random

user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe', 'is_superuser': True, 'is_staff': True},
]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 30
    ENTRY_COUNT = 80
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.create_entries_for_users()
        self.users = User.objects.all()

    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_superuser(data)

    def generate_random_users(self):
        user_count = User.objects.count()
        while  user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            self.generate_user()
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})
       
    def try_create_user(self, data):
        try:
            self.create_user(data)
        except:
            pass
    
    def try_create_superuser(self, data):
        try:
            self.create_superuser(data)
        except:
            pass

    def create_user(self, data):
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
    
    def create_superuser(self, data):
        User.objects.create_superuser(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
    
    def create_entries_for_users(self):
        users = User.objects.all()
        index = 0
        for user in users:
            print(f"Seeding entries for user {index}/{self.USER_COUNT}", end='\r')
            self.create_entries_for_user(user)
            index += 1
    
    def create_entries_for_user(self, user):
        now = datetime.now(pytz.UTC)
        start_date = now - timedelta(days=365)

        for _ in range(self.ENTRY_COUNT):
            entry_date = start_date + timedelta(days=1)
            if entry_date > now:
                break

            title = self.faker.sentence(nb_words=6)
            text = self.faker.paragraph(nb_sentences=5)
            mood_int = randint(0, 50)
            mood = mood_int / 10.0
            template_decider = random()
            if template_decider < 0.1:
                template_decider = True
            else:
                template_decider = False

            Entry.objects.create(
                user=user,
                title=title,
                text=text,
                date_created=entry_date,
                mood=mood,
                is_template=template_decider
            )

            start_date = entry_date 

def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'

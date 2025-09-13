from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from libgravatar import Gravatar

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    achievements = models.ManyToManyField('Achievement', blank=True)
    last_login = models.DateTimeField(default=timezone.now)
    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']  

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)
    
    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)

        if created:
            # Create three default achievements for the new user
            achievements = Achievement.objects.bulk_create([
                Achievement(name='A Penny for your Thoughts?', description='Write 10 entries into your journal', value = 10,reward="dark"),
                Achievement(name='Reflections of the Mind', description='Write 20 entries into your journal',value = 20,reward="light"),
                Achievement(name='Inner Peace', description='Write 30 entries into your journal',value = 30,reward="red"),
            ])
            self.achievements.add(*achievements)

class Entry(models.Model):
    """Model used for entry creation, bookmarking, and editing"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    image = models.ImageField(upload_to = 'images/', null = True, blank = True)
    date_created = models.DateTimeField(default=timezone.now)
    bookmarked = models.BooleanField(default=False)
    mood = models.FloatField(default=2.5)
    is_template = models.BooleanField(default=False)
    
class Achievement(models.Model):
    """Model used for achievement creation and completion"""

    name = models.CharField(max_length=100)
    description = models.TextField()
    reward = models.CharField(max_length=100)
    date_acquired = models.DateTimeField(default=timezone.now)
    value = models.IntegerField(default = 0)
    completed = models.IntegerField(default=0)
    percentage_completed = models.IntegerField(default=0)
    is_achieved = models.BooleanField(default=False)
    
    def update_is_achieved(self):
        if self.completed >= self.value:
            self.is_achieved = True
            self.save()

class Reminder(models.Model):
    """Model used for reminders sent to the user"""
    
    name = models.CharField(max_length=100)
    description = description = models.TextField()
    value = models.IntegerField(default = 0)
    date_created = models.DateTimeField(default=timezone.now)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
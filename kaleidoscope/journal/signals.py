from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Entry, User

@receiver(post_save, sender=User)
def create_user_templates(sender, instance, created, **kwargs):
    if created:
        templates = [
            {"title": "Gratitude Journal Template", 
            "text": """Three things I'm grateful for today:
             1. 
             2. 
             3. 
             
             Postive experiences I had today: """, 
            "is_template": True},
            {"title": "Daily Reflection Template", 
             "text": """Today's highlights:

             Challenges faced: 

             What I learned today: """, 
             "is_template": True},
            {"title": "Emotional Check-in Template", 
             "text": """How do I feel right now:

             What triggered these feelings: 

             What can I do to improve my mood: """, 
             "is_template": True},
            {"title": "Mindfulness Practice Template", 
             "text": """Today's mindfulness activity:

             How did it make me feel:
             
             Reflections on staying present: """, 
             "is_template": True},
            {"title": "Goal Setting Template", 
             "text": """Three goals for this week:
             1.
             2.
             3.
             
             Actions to achieve these goals: """, 
             "is_template": True},

        ]
        for template in templates:
            Entry.objects.create(user=instance, **template)

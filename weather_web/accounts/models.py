from django.db import models
from django.contrib import auth
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


class UserPreference(models.Model):
    degrees_choices = [('C', 'Celsius'),
                       ('F', 'Fahrenheit')
                       ]
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    degrees = models.CharField(
        max_length=255, choices=degrees_choices, default='C')

    def __str__(self):
        return self.user.username + '_preferences'


@receiver(post_save, sender=get_user_model())
def preference_create(sender, instance=None, created=False, **kwargs):
    if created:
        UserPreference.objects.create(user=instance)
# https://stackoverflow.com/questions/52196365/django-automatically-create-a-model-instance-when-another-model-instance-is-cr

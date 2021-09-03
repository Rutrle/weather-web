from django.db import models
from accounts import models as account_models
from django.utils import timezone


class Place(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(
        account_models.User, related_name='%(class)susername', on_delete=models.SET_NULL, null=True)
    longtitude = models.DecimalField(max_digits=8, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

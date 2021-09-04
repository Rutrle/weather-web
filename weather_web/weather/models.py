from django.db import models
from accounts import models as account_models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class Place(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(
        get_user_model(), related_name='%(class)susername', on_delete=models.SET_NULL, null=True)
    longtitude = models.DecimalField(max_digits=8, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

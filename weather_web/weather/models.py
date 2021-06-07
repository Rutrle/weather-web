from django.db import models

# Create your models here.


class Place(models.Model):
    name = models.CharField(max_length=255, unique=True)
    longtitude = models.DecimalField(max_digits=8, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name

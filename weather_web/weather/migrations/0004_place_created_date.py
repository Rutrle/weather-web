# Generated by Django 3.2.3 on 2021-09-03 19:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_alter_place_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
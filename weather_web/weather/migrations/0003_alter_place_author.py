# Generated by Django 3.2.3 on 2021-09-03 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('weather', '0002_place_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='placeusername', to='accounts.user'),
        ),
    ]

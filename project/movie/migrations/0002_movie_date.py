# Generated by Django 4.0.3 on 2022-03-03 20:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
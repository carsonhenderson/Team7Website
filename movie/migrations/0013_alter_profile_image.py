# Generated by Django 4.0.3 on 2022-04-04 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0012_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.png', upload_to='movie/static/images/profile'),
        ),
    ]

# Generated by Django 2.0.8 on 2018-08-08 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('its', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='model_name',
            field=models.CharField(default='Optiplex 755', max_length=20),
        ),
    ]

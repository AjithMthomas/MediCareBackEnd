# Generated by Django 4.2.2 on 2023-06-07 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slots',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
    ]

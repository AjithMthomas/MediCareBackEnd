# Generated by Django 4.2.2 on 2023-06-22 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctors', '0008_alter_doctors_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctors',
            name='fee',
            field=models.IntegerField(),
        ),
    ]

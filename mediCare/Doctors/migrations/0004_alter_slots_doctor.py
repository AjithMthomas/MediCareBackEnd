# Generated by Django 4.2.2 on 2023-06-12 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doctors', '0003_blogs_delete_students_alter_doctors_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slots',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctors.doctors'),
        ),
    ]
# Generated by Django 4.0.2 on 2022-09-25 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0061_bookslot_booked_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookslot',
            name='Booked_on',
        ),
    ]
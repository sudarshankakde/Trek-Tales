# Generated by Django 4.1.1 on 2022-10-02 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0086_alter_bookslot_tripid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookslot',
            name='aadhaar_number',
        ),
        migrations.RemoveField(
            model_name='bookslot',
            name='age',
        ),
    ]

# Generated by Django 4.0.2 on 2022-08-11 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0035_alter_bookslot_canceled_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookslot',
            name='canceled_on',
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-16 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0009_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='Contact_on',
            field=models.DateField(auto_created=True, auto_now=True),
        ),
    ]

# Generated by Django 4.0.2 on 2022-08-11 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0036_remove_bookslot_canceled_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookslot',
            name='canceled',
            field=models.BooleanField(default=False),
        ),
    ]

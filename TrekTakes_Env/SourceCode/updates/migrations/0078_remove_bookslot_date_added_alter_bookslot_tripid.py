# Generated by Django 4.0.2 on 2022-09-25 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0077_alter_bookslot_tripid_alter_bookslot_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookslot',
            name='date_added',
        ),
        migrations.AlterField(
            model_name='bookslot',
            name='TripId',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
    ]

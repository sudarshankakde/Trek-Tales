# Generated by Django 4.1.1 on 2022-10-04 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0099_remove_bookslot_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookslot',
            name='aadhaar_number',
            field=models.IntegerField(editable=False),
        ),
    ]
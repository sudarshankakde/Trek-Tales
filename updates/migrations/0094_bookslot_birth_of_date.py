# Generated by Django 4.1.1 on 2022-10-02 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0093_bookslot_aadhaar_number_bookslot_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookslot',
            name='birth_of_date',
            field=models.DateField(default=1, editable=False),
            preserve_default=False,
        ),
    ]

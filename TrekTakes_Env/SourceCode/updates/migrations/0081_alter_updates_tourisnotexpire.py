# Generated by Django 4.1.1 on 2022-09-28 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0080_alter_refund_cancelation_reason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updates',
            name='TourIsNotExpire',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]

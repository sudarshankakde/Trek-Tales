# Generated by Django 4.1.1 on 2022-10-02 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0085_alter_bookslot_razorpay_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookslot',
            name='TripId',
            field=models.CharField(editable=False, max_length=20),
        ),
    ]

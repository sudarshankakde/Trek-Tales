# Generated by Django 4.1.1 on 2022-10-02 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0084_alter_bookslot_aadhaar_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookslot',
            name='razorpay_payment_id',
            field=models.CharField(editable=False, max_length=50, null=True),
        ),
    ]

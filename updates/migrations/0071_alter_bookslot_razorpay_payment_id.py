# Generated by Django 4.0.2 on 2022-09-25 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0070_alter_bookslot_razorpay_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookslot',
            name='razorpay_payment_id',
            field=models.CharField(default=2, editable=False, max_length=50, unique_for_date=True),
            preserve_default=False,
        ),
    ]

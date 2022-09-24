# Generated by Django 4.0.2 on 2022-08-10 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0031_bookslot_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookslot',
            name='Payment_Status',
            field=models.CharField(default='null', max_length=10),
        ),
        migrations.AlterField(
            model_name='bookslot',
            name='razorpay_order_id',
            field=models.CharField(editable=False, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bookslot',
            name='razorpay_payment_id',
            field=models.CharField(editable=False, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bookslot',
            name='razorpay_signature',
            field=models.CharField(editable=False, max_length=50, null=True),
        ),
    ]

# Generated by Django 4.0.2 on 2022-08-10 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0030_newsletter_subscriber_alter_updates_tour_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookslot',
            name='razorpay_order_id',
            field=models.CharField(default=1, editable=False, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookslot',
            name='razorpay_payment_id',
            field=models.CharField(default=1, editable=False, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookslot',
            name='razorpay_signature',
            field=models.CharField(default=1, editable=False, max_length=50),
            preserve_default=False,
        ),
    ]

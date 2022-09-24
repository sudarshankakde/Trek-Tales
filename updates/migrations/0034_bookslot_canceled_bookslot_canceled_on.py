# Generated by Django 4.0.2 on 2022-08-11 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0033_alter_bookslot_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookslot',
            name='canceled',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='bookslot',
            name='canceled_on',
            field=models.DateField(blank=True, default=1),
            preserve_default=False,
        ),
    ]

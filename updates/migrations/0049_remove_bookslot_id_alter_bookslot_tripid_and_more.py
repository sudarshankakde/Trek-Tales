# Generated by Django 4.0.2 on 2022-09-16 13:43

import autoslug.fields
from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0048_updates_slug_alter_updates_heading'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookslot',
            name='id',
        ),
        migrations.AlterField(
            model_name='bookslot',
            name='TripId',
            field=models.CharField(editable=False, max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bookslot',
            name='razorpay_payment_id',
            field=models.CharField(editable=False, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='organizer',
            name='image',
            field=models.ImageField(upload_to='DataBase/tours/Images/organizers'),
        ),
        migrations.AlterField(
            model_name='testimonials',
            name='ReviewerImage',
            field=models.ImageField(upload_to='DataBase/tours/Images/Testimonials', verbose_name="reviewer's image"),
        ),
        migrations.AlterField(
            model_name='updates',
            name='Tour_image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=False, quality=100, scale=None, size=[375, 225], upload_to='DataBase/tours/Images/tour', verbose_name='tour image shown on cards.'),
        ),
        migrations.AlterField(
            model_name='updates',
            name='Tumbnail',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=False, quality=100, scale=None, size=[800, 450], upload_to='DataBase/tours/Images/tour/tubnail', verbose_name='detailed thubnail'),
        ),
        migrations.AlterField(
            model_name='updates',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='Heading'),
        ),
    ]

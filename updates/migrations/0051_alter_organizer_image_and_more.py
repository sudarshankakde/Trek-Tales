# Generated by Django 4.0.2 on 2022-09-17 13:18

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0050_bookslot_id_alter_bookslot_tripid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizer',
            name='image',
            field=models.ImageField(upload_to='tours/Images/organizers'),
        ),
        migrations.AlterField(
            model_name='testimonials',
            name='ReviewerImage',
            field=models.ImageField(upload_to='Images/Testimonials', verbose_name="reviewer's image"),
        ),
        migrations.AlterField(
            model_name='updates',
            name='Tour_image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=False, quality=100, scale=None, size=[375, 225], upload_to='tours/Images/tour', verbose_name='tour image shown on cards.'),
        ),
        migrations.AlterField(
            model_name='updates',
            name='Tumbnail',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=False, quality=100, scale=None, size=[800, 450], upload_to='tours/Images/tour/tubnail', verbose_name='detailed thubnail'),
        ),
    ]

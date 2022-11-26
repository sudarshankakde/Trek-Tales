# Generated by Django 4.0.2 on 2022-08-04 16:12

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0022_delete_tourimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updates',
            name='Tour_image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=False, quality=100, scale=None, size=[285, 160], upload_to='tour', verbose_name='tour image shown on cards.'),
        ),
        migrations.AlterField(
            model_name='updates',
            name='Tumbnail',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=False, quality=100, scale=None, size=[285, 160], upload_to='tour/tubnail', verbose_name='detailed thubnail'),
        ),
        migrations.AlterField(
            model_name='updates',
            name='tour_on_date',
            field=models.CharField(max_length=100, verbose_name='Month , form - to'),
        ),
    ]
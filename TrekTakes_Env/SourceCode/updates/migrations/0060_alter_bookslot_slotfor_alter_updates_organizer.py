# Generated by Django 4.0.2 on 2022-09-24 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0059_alter_bookslot_amount_alter_bookslot_slotfor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookslot',
            name='slotFor',
            field=models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.PROTECT, to='updates.updates'),
        ),
        migrations.AlterField(
            model_name='updates',
            name='Organizer',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='updates.organizer'),
        ),
    ]

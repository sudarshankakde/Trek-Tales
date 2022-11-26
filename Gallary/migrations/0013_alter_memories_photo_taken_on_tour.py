# Generated by Django 4.0.2 on 2022-09-24 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0060_alter_bookslot_slotfor_alter_updates_organizer'),
        ('Gallary', '0012_alter_memories_photo_taken_on_tour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memories',
            name='photo_taken_on_tour',
            field=models.ForeignKey(default='unknown tour', null=True, on_delete=django.db.models.deletion.PROTECT, to='updates.updates'),
        ),
    ]
# Generated by Django 4.1.1 on 2022-10-02 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0097_alter_bookslot_birth_of_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookslot',
            name='birth_of_date',
            field=models.DateField(editable=False),
        ),
    ]

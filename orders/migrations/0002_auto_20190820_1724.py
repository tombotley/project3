# Generated by Django 2.0.3 on 2019-08-20 16:24

from django.db import migrations


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Extras',
            new_name='Extra',
        ),
        migrations.RenameModel(
            old_name='PricedPizza',
            new_name='PizzaPrice',
        ),
        migrations.RenameModel(
            old_name='PricedPlatter',
            new_name='PlatterPrice',
        ),
        migrations.RenameModel(
            old_name='PricedSub',
            new_name='SubPrice',
        ),
    ]

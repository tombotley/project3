# Generated by Django 2.0.3 on 2019-09-13 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.IntegerField(),
        ),
    ]

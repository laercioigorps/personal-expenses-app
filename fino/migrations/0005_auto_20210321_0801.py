# Generated by Django 3.1.7 on 2021-03-21 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fino', '0004_cattegory_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]

# Generated by Django 3.2.4 on 2021-06-13 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210613_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='phonenum',
            field=models.CharField(default=0, max_length=100),
        ),
    ]

# Generated by Django 3.2.4 on 2021-06-13 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210613_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='korname',
            field=models.CharField(max_length=100),
        ),
    ]

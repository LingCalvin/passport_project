# Generated by Django 3.0.6 on 2020-05-28 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pclients', '0002_auto_20200528_0815'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pclient',
            old_name='name',
            new_name='company_name',
        ),
        migrations.AddField(
            model_name='pclient',
            name='first_name',
            field=models.CharField(default='null', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pclient',
            name='last_name',
            field=models.CharField(default='last name', max_length=32),
            preserve_default=False,
        ),
    ]
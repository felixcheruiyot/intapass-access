# Generated by Django 4.2.3 on 2023-07-16 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='access',
            name='root_access',
            field=models.BooleanField(default=False),
        ),
    ]

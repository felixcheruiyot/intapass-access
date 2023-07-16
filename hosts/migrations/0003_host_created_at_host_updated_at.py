# Generated by Django 4.2.3 on 2023-07-16 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0002_alter_host_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

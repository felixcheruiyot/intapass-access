# Generated by Django 4.2.3 on 2023-07-16 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='label',
            field=models.SlugField(help_text='Server name or identifier', max_length=45, unique=True),
        ),
    ]
# Generated by Django 3.2.9 on 2022-07-14 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='subcatgeory',
            new_name='subcategory',
        ),
    ]
# Generated by Django 3.2.4 on 2021-06-22 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210622_2044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-id']},
        ),
    ]
# Generated by Django 2.2.2 on 2019-06-30 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20190630_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='literary_awards',
            field=models.TextField(blank=True),
        ),
    ]
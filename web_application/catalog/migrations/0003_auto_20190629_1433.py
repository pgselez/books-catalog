# Generated by Django 2.2.2 on 2019-06-29 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20190629_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]

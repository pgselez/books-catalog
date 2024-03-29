# Generated by Django 2.2.2 on 2019-07-28 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_auto_20190728_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='goodreads_id',
            field=models.IntegerField(default=111),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='author',
            name='biography',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='authors'),
        ),
        migrations.AlterField(
            model_name='author',
            name='photo_origin',
            field=models.URLField(max_length=255, null=True),
        ),
    ]

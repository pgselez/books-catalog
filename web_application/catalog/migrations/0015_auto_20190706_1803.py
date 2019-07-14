# Generated by Django 2.2.2 on 2019-07-06 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_auto_20190706_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='poster',
        ),
        migrations.RemoveField(
            model_name='character',
            name='photo',
        ),
        migrations.AddField(
            model_name='photo',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Book'),
        ),
        migrations.AddField(
            model_name='photo',
            name='character',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Character'),
        ),
    ]
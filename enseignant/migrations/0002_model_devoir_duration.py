# Generated by Django 5.0.3 on 2024-05-11 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enseignant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='model_devoir',
            name='duration',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]

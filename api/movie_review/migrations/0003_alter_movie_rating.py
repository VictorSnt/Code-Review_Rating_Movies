# Generated by Django 5.0.2 on 2024-02-27 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_review', '0002_movie_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.FloatField(default=None, null=True, verbose_name='Nota'),
        ),
    ]

# Generated by Django 5.0.2 on 2024-02-27 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_review', '0005_alter_gender_created_at_avaliation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avaliation',
            name='rate',
            field=models.IntegerField(),
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-31 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0004_trip_average_words_per_sentence_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='Meta_robots_4',
        ),
    ]

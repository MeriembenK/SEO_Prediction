# Generated by Django 4.2.6 on 2023-11-02 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0006_remove_trip_meta_keywords2_alter_trip_errors_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='Meta_keywords2_length',
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-13 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0024_remove_data_date_added_data_date_of_birth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='date_of_birth',
            new_name='Date_added',
        ),
    ]
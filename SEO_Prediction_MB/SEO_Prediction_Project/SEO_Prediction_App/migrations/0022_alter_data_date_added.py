# Generated by Django 4.2.6 on 2023-11-13 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0021_rename_date_added_data_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='Date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

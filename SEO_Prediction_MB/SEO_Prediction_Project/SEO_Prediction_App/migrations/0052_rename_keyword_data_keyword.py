# Generated by Django 4.2.6 on 2024-01-30 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0051_remove_data_url_keyword_data_keyword'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='keyword',
            new_name='Keyword',
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-20 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0030_rename_url_score_data_url_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='Keyword',
            new_name='Thekeyword',
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-14 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0028_alter_data_score_1fr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='keyword',
            new_name='Keyword',
        ),
    ]
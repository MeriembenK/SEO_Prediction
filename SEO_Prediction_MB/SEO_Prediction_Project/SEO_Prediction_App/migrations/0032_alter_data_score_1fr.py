# Generated by Django 4.2.6 on 2023-11-20 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0031_rename_keyword_data_thekeyword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='Score_1fr',
            field=models.FloatField(null=True),
        ),
    ]

# Generated by Django 4.2.6 on 2024-06-19 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0070_urlpredected_keyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlpredected',
            name='date_test',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='urlpredected',
            name='hour_test',
            field=models.TimeField(null=True),
        ),
    ]

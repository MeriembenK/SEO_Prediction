# Generated by Django 4.2.6 on 2024-05-29 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0063_remove_keyword_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SEO_Prediction_App.user'),
        ),
    ]

# Generated by Django 4.2.6 on 2023-12-26 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0035_rename_keyword_keyword_keyword_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword_Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Keyword_url', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='keyword',
            old_name='Keyword_url',
            new_name='Keyword',
        ),
    ]
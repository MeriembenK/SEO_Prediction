# Generated by Django 4.2.6 on 2023-11-07 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0013_remove_data_canonical_link_element1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keyword',
            old_name='keyword',
            new_name='Keyword',
        ),
        migrations.AddField(
            model_name='data',
            name='Canonical_link_element1',
            field=models.CharField(max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Canonical_link_element2',
            field=models.CharField(max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Closest_Similarity_Match',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Content_type',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Cookies',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Crawl_Timestamp',
            field=models.CharField(max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Grammar_Errors',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='HTTP_Version',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='HTTP_rel_next_1',
            field=models.CharField(max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='HTTP_rel_prev_1',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Hash',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Http_code_babbar',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Indexability_Status_y',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Indexability_status_x',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Indexability_x',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Indexability_y',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Link_score',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Meta_Refresh_1',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Meta_Robots_1_score',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='NoNear_Duplicates',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Position',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Readability',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Redirect_URL',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Redirect_type',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Spelling_Errors',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Status',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Status_code',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Type_1',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='URL_Encoded_Address',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='Url_score',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='X_robots_tag1',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='amphtml_link_element',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='rel_next_1',
            field=models.CharField(max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='rel_prev_1',
            field=models.CharField(max_length=350, null=True),
        ),
    ]

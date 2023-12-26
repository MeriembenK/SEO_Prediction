# Generated by Django 4.2.6 on 2023-11-28 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0032_alter_data_score_1fr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='Desktop_cumulative_layout_shift_lab',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Desktop_cumulative_layout_shift_terrain',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Desktop_first_contentful_paint_lab',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Desktop_first_contentful_paint_terrain',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Desktop_first_input_delay_terain',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Desktop_largest_contentful_paint_lab',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Desktop_largest_contentful_paint_terrain',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Desktop_speed_index_lab',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Desktop_time_to_interactive_lab',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='Desktop_total_blocking_time_lab',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
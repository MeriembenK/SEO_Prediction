# Generated by Django 4.2.6 on 2023-12-20 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SEO_Prediction_App', '0033_alter_data_desktop_cumulative_layout_shift_lab_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data_Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Thekeyword', models.CharField(max_length=2150, null=True)),
                ('Position', models.PositiveIntegerField(null=True)),
                ('Url', models.CharField(max_length=200, null=True)),
                ('Top10', models.BooleanField(null=True)),
                ('Http_code_babbar', models.FloatField(null=True)),
                ('Ttfb_babbar', models.FloatField(null=True)),
                ('Page_value_babbar', models.FloatField(null=True)),
                ('Page_trust_babbar', models.FloatField(null=True)),
                ('Semantic_value_babbar', models.FloatField(null=True)),
                ('Backlinks_babbar', models.FloatField(null=True)),
                ('Backlinks_host_babbar', models.FloatField(null=True)),
                ('Host_outlinks_babbar', models.FloatField(null=True)),
                ('Outlinks_babbar', models.FloatField(null=True)),
                ('Desktop_first_contentful_paint_terrain', models.FloatField(blank=True, null=True)),
                ('Desktop_first_input_delay_terain', models.FloatField(blank=True, null=True)),
                ('Desktop_largest_contentful_paint_terrain', models.FloatField(blank=True, null=True)),
                ('Desktop_cumulative_layout_shift_terrain', models.FloatField(blank=True, null=True)),
                ('Desktop_first_contentful_paint_lab', models.FloatField(blank=True, null=True)),
                ('Desktop_speed_index_lab', models.FloatField(blank=True, null=True)),
                ('Desktop_largest_contentful_paint_lab', models.FloatField(blank=True, null=True)),
                ('Desktop_time_to_interactive_lab', models.FloatField(blank=True, null=True)),
                ('Desktop_total_blocking_time_lab', models.FloatField(blank=True, null=True)),
                ('Desktop_cumulative_layout_shift_lab', models.FloatField(blank=True, null=True)),
                ('Mobile_first_contentful_paint_terrain', models.FloatField(blank=True, null=True)),
                ('Mobile_first_input_delay_terain', models.FloatField(null=True)),
                ('Mobile_largest_contentful_paint_terrain', models.FloatField(null=True)),
                ('Mobile_cumulative_layout_shift_terrain', models.FloatField(null=True)),
                ('Mobile_first_contentful_paint_lab', models.FloatField(null=True)),
                ('Mobile_speed_index_lab', models.FloatField(null=True)),
                ('Mobile_largest_contentful_paint_lab', models.FloatField(null=True)),
                ('Mobile_time_to_interactive_lab', models.FloatField(null=True)),
                ('Mobile_total_blocking_time_lab', models.FloatField(null=True)),
                ('Mobile_cumulative_layout_shift_lab', models.FloatField(null=True)),
                ('SOSEO_yourtext_guru', models.FloatField(null=True)),
                ('DSEO_yourtext_guru', models.FloatField(null=True)),
                ('Score_1fr', models.FloatField(null=True)),
                ('Content_type', models.CharField(max_length=150, null=True)),
                ('Status_code', models.CharField(max_length=150, null=True)),
                ('Status', models.CharField(max_length=150, null=True)),
                ('Indexability_x', models.CharField(max_length=150, null=True)),
                ('Indexability_status_x', models.CharField(max_length=150, null=True)),
                ('Title1', models.CharField(max_length=350, null=True)),
                ('Title1_length', models.CharField(max_length=350, null=True)),
                ('Title1_pixel_width', models.CharField(max_length=150, null=True)),
                ('Title2', models.CharField(max_length=150, null=True)),
                ('Title2_length', models.CharField(max_length=150, null=True)),
                ('Title2_pixel_width', models.CharField(max_length=150, null=True)),
                ('Meta_description1', models.CharField(max_length=150, null=True)),
                ('Meta_description1_length', models.CharField(max_length=350, null=True)),
                ('Meta_description1_Pixel_width', models.CharField(max_length=350, null=True)),
                ('Meta_description2', models.CharField(max_length=150, null=True)),
                ('Meta_description2_length', models.CharField(max_length=350, null=True)),
                ('Meta_description2_Pixel_width', models.CharField(max_length=350, null=True)),
                ('Meta_Keywords1', models.CharField(max_length=350, null=True)),
                ('Meta_keywords1_length', models.CharField(max_length=350, null=True)),
                ('H1_1', models.CharField(max_length=150, null=True)),
                ('H1_1_length', models.CharField(max_length=350, null=True)),
                ('H1_2', models.CharField(max_length=150, null=True)),
                ('H1_2_length', models.CharField(max_length=150, null=True)),
                ('H2_1', models.CharField(max_length=350, null=True)),
                ('H2_1_length', models.CharField(max_length=350, null=True)),
                ('H2_2', models.CharField(max_length=150, null=True)),
                ('H2_2_length', models.CharField(max_length=350, null=True)),
                ('Meta_robots_1', models.CharField(max_length=150, null=True)),
                ('Meta_robots_2', models.CharField(max_length=150, null=True)),
                ('Meta_robots_3', models.CharField(max_length=150, null=True)),
                ('X_robots_tag1', models.CharField(max_length=150, null=True)),
                ('Meta_Refresh_1', models.CharField(max_length=150, null=True)),
                ('Canonical_link_element1', models.CharField(max_length=350, null=True)),
                ('Canonical_link_element2', models.CharField(max_length=350, null=True)),
                ('rel_next_1', models.CharField(max_length=350, null=True)),
                ('rel_prev_1', models.CharField(max_length=350, null=True)),
                ('HTTP_rel_next_1', models.CharField(max_length=350, null=True)),
                ('HTTP_rel_prev_1', models.CharField(max_length=150, null=True)),
                ('amphtml_link_element', models.CharField(max_length=150, null=True)),
                ('Size_bytes', models.FloatField(null=True)),
                ('Word_count', models.FloatField(null=True)),
                ('Sentence_Count', models.FloatField(null=True)),
                ('Average_words_per_sentence', models.CharField(max_length=150, null=True)),
                ('Flesch_reading_ease_score', models.FloatField(null=True)),
                ('Readability', models.CharField(max_length=30, null=True)),
                ('Text_ratio', models.CharField(max_length=30, null=True)),
                ('Crawl_depth', models.FloatField(null=True)),
                ('Link_score', models.FloatField(null=True)),
                ('Inlinks', models.FloatField(null=True)),
                ('Unique_inlinks', models.FloatField(null=True)),
                ('Unique_JS_inlinks', models.CharField(max_length=30, null=True)),
                ('of_Total', models.FloatField(null=True)),
                ('Outlinks', models.FloatField(null=True)),
                ('Unique_Outlinks', models.FloatField(null=True)),
                ('Unique_JS_Outlinks', models.CharField(max_length=30, null=True)),
                ('External_Outlinks', models.FloatField(null=True)),
                ('Unique_External_Outlinks', models.FloatField(null=True)),
                ('Unique_External_JS_Outlinks', models.FloatField(null=True)),
                ('Closest_Similarity_Match', models.FloatField(null=True)),
                ('NoNear_Duplicates', models.FloatField(null=True)),
                ('Spelling_Errors', models.FloatField(null=True)),
                ('Grammar_Errors', models.FloatField(null=True)),
                ('Hash', models.CharField(max_length=150, null=True)),
                ('Response_time', models.CharField(max_length=150, null=True)),
                ('Last_modified', models.CharField(max_length=150, null=True)),
                ('Redirect_URL', models.CharField(max_length=150, null=True)),
                ('Redirect_type', models.CharField(max_length=150, null=True)),
                ('Cookies', models.CharField(max_length=150, null=True)),
                ('HTTP_Version', models.FloatField(null=True)),
                ('URL_Encoded_Address', models.CharField(max_length=150, null=True)),
                ('Crawl_Timestamp', models.CharField(max_length=350, null=True)),
                ('Errors', models.CharField(max_length=150, null=True)),
                ('Warnings', models.FloatField(null=True)),
                ('Total_Types', models.FloatField(null=True)),
                ('Unique_Types', models.CharField(max_length=150, null=True)),
                ('Type_1', models.FloatField(null=True)),
                ('Indexability_y', models.CharField(max_length=150, null=True)),
                ('Indexability_Status_y', models.CharField(max_length=150, null=True)),
                ('Title1_score', models.FloatField(null=True)),
                ('Meta_Description1_score', models.FloatField(null=True)),
                ('Meta_Keywords1_score', models.FloatField(null=True)),
                ('H1_1_score', models.FloatField(null=True)),
                ('H1_2_score', models.FloatField(null=True)),
                ('H2_1_score', models.FloatField(null=True)),
                ('H2_2_score', models.FloatField(null=True)),
                ('Meta_Robots_1_score', models.FloatField(null=True)),
                ('Date_added', models.DateField(blank=True, null=True)),
                ('Url_Score', models.FloatField(null=True)),
            ],
        ),
    ]

# SEO_Prediction_App/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

class User(AbstractUser):
    # Ajoutez des champs personnalisés si nécessaire
   
    # Spécifiez des noms de relation inverses personnalisés pour éviter les conflits
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)
  

class Keyword(models.Model):
    Keyword = models.CharField(max_length=255, null=True)


class Data(models.Model):
    
    Thekeyword = models.CharField(max_length=2150, null=True)  # Champ pour Keyword
    Keyword = models.CharField(max_length=150, null=True) # champ pour Keyword principale
    Position = models.PositiveIntegerField(null=True)  # Champ pour la position
    Url = models.CharField(max_length=200, null=True)  # Champ pour l'URL
    Top10 = models.BooleanField(null=True)  # Champ pour Top 10 (0 ou 1)
    Http_code_babbar = models.FloatField(null=True)  # Champ pour HTTP Code BABBAR
    Ttfb_babbar = models.FloatField(null=True)  # Champ pour TTFB BABBAR (en ms) 
    Page_value_babbar = models.FloatField(null=True)  # Champ pour Page Value BABBAR
    Page_trust_babbar = models.FloatField(null=True) # Champ pour Page Trust BABBAR
    Semantic_value_babbar = models.FloatField(null=True)# Champ pour Semantic Value BABBARs
    Backlinks_babbar = models.FloatField(null=True)  # Champ pour Backlinks BABBAR
    Backlinks_host_babbar = models.FloatField(null=True)  # Champ pour Backlinks Host BABBAR
    Host_outlinks_babbar = models.FloatField(null=True)  # Champ pour Host Outlinks BABBAR
    Outlinks_babbar = models.FloatField(null=True)  # Champ pour Outlinks BABBAR
    Desktop_first_contentful_paint_terrain = models.FloatField(null=True,  blank=True) # Champ pour Desktop First Contentful Paint Terrain
    Desktop_first_input_delay_terain = models.FloatField(null=True, blank= True) # Champ pour Desktop First Input delay Terain
    Desktop_largest_contentful_paint_terrain = models.FloatField(null=True, blank= True) # Champ pour Desktop Largest Contentful Paint Terrain
    Desktop_cumulative_layout_shift_terrain = models.FloatField(null=True, blank= True) # Champ pour Desktop Cumulative Layout Shift Terrain
    Desktop_first_contentful_paint_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop First Contentful Paint Lab
    Desktop_speed_index_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop Speed Index Lab
    Desktop_largest_contentful_paint_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop Largest Contentful Paint Lab
    Desktop_time_to_interactive_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop Time to Interactive Lab
    Desktop_total_blocking_time_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop Total Blocking Time Lab
    Desktop_cumulative_layout_shift_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop Cumulative Layout Shift Lab
    Mobile_first_contentful_paint_terrain =  models.FloatField(null=True, blank=True) # Champ pour Mobile Contentful Paint Terrain
    Mobile_first_input_delay_terain = models.FloatField(null=True) # Champ pour Mobile First Input Delay Terain
    Mobile_largest_contentful_paint_terrain =  models.FloatField(null=True) # Champ pour Mobile Largest Contentful Paint Terrain
    Mobile_cumulative_layout_shift_terrain = models.FloatField(null=True) # Champ pour Mobile Cumulative Layout Shift Terrain 
    Mobile_first_contentful_paint_lab = models.FloatField(null=True) # Champ pour Mobile First Contentful Paint Lab
    Mobile_speed_index_lab = models.FloatField(null=True) # Champ pour Mobile Speed Index Lab
    Mobile_largest_contentful_paint_lab = models.FloatField(null=True) # Champ pour Mobile Largest Contentful Paint Lab
    Mobile_time_to_interactive_lab = models.FloatField(null=True) # Champ pour Mobile Time to Interactive Lab
    Mobile_total_blocking_time_lab = models.FloatField(null=True) # Champ pour Mobile Total Blocking Time Lab
    Mobile_cumulative_layout_shift_lab = models.FloatField(null=True) # Champ pour Mobile Cumulative Layout Shift Lab
    SOSEO_yourtext_guru = models.FloatField(null=True)# Champ pour SOSEO yourtext_guru
    DSEO_yourtext_guru = models.FloatField(null=True)# Champ pour DSEO yourtext_guru
    Score_1fr = models.FloatField(null=True) # Champ pour Score_1fr
    Content_type = models.CharField(max_length=150, null=True)  # Champ pour Content Type
    Status_code = models.CharField(max_length=150, null=True)  # Champ pour Status Code
    Status = models.CharField(max_length=150, null=True)  # Champ pour Status
    Indexability_x =  models.CharField(max_length=150, null=True)  # Champ pour Indexability_x
    Indexability_status_x = models.CharField(max_length=150, null=True)  # Champ pour Indexability Status_x
    Title1 = models.CharField(max_length=350, null=True)  # Champ pour Title 1
    Title1_length = models.CharField(max_length=350, null=True)  # Champ pour Title 1 Length
    Title1_pixel_width = models.CharField(max_length=150, null=True) # Champ pour Title 1 Pixel Width
    Title2 = models.CharField(max_length=150, null=True) # Champ pour Title 2
    Title2_length = models.CharField(max_length=150, null=True)  # Champ pour Title 2 Length
    Title2_pixel_width = models.CharField(max_length=150, null=True) # Champ pour Title 2 Pixel Width
    Meta_description1 = models.CharField(max_length=150, null=True) # Champ pour Meta Description 1
    Meta_description1_length =  models.CharField(max_length=350, null=True) # Champ pour Meta Description 1 Length
    Meta_description1_Pixel_width =  models.CharField(max_length=350, null=True) # Champ pour Meta Description 1 Pixel Width
    Meta_description2 = models.CharField(max_length=150, null=True) # Champ pour Meta Description 2
    Meta_description2_length =  models.CharField(max_length=350, null=True) # Champ pour Meta Description 2 Length
    Meta_description2_Pixel_width =  models.CharField(max_length=350, null=True) # Champ pour Meta Description 2 Pixel Width
    Meta_Keywords1 = models.CharField(max_length=350, null=True) # Champ pour Meta Keywords 1
    Meta_keywords1_length = models.CharField(max_length=350, null=True) # Champ pour Meta Keywords 1 Length
    H1_1  = models.CharField(max_length=150, null=True) # Champ pour H1-1
    H1_1_length = models.CharField(max_length=350, null=True) # Champ pour H1-1 Length
    H1_2 = models.CharField(max_length=150, null=True) # Champ pour H1-2
    H1_2_length = models.CharField(max_length=150, null=True) # Champ pour H1-2 Length
    H2_1 = models.CharField(max_length=350, null=True) # Champ pour H2-1
    H2_1_length = models.CharField(max_length=350, null=True) # Champ pour H2-1 Length
    H2_2 = models.CharField(max_length=150, null=True) # Champ pour H2-2 
    H2_2_length = models.CharField(max_length=350, null=True) # Champ pour H2-2 Length
    Meta_robots_1 = models.CharField(max_length=150, null=True) # Champ pour Meta Robots 1
    Meta_robots_2 = models.CharField(max_length=150, null=True) # Champ pour Meta Robots 2
    Meta_robots_3 = models.CharField(max_length=150, null=True) # Champ pour Meta Robots 3                                                           
    X_robots_tag1 = models.CharField(max_length=150, null=True) # Champ pour X-Robots-Tag 1
    Meta_Refresh_1 = models.CharField(max_length=150, null=True) # Champ pour Meta Refresh 1
    Canonical_link_element1 = models.CharField(max_length=350, null=True) # Champ pour Canonical Link Element 1
    Canonical_link_element2 = models.CharField(max_length=350, null=True) # Champ pour Canonical Link Element 2
    rel_next_1 = models.CharField(max_length=350, null=True) # Champ pour rel="next" 1
    rel_prev_1 = models.CharField(max_length=350, null=True) # Champ pour rel="prev" 1
    HTTP_rel_next_1 = models.CharField(max_length=350, null=True) # Champ pour HTTP rel="next" 1
    HTTP_rel_prev_1 = models.CharField(max_length=150, null=True) # Champ pour HTTP rel="prev" 1
    amphtml_link_element = models.CharField(max_length=150, null=True) # Champ pour amphtml Link Element
    Size_bytes = models.FloatField(null=True)# Champ pour Size (bytes)
    Word_count = models.FloatField(null=True)# Champ pour Word Count
    Sentence_Count = models.FloatField(null=True)# Champ pour sentence Count
    Average_words_per_sentence = models.CharField(max_length=150, null=True) # Champ pour Average Words Per Sentence
    Flesch_reading_ease_score = models.FloatField(null=True)# Champ pour Flesch Reading Ease Score
    Readability = models.CharField(max_length=30, null=True) # Champ pour Readability
    Text_ratio = models.CharField(max_length=30, null=True) # Champ pour Text Ratio
    Crawl_depth = models.FloatField(null=True)# Champ pour Crawl Depth
    Link_score = models.FloatField(null=True)# Champ pour Link Score
    Inlinks =  models.FloatField(null=True)# Champ pour Inlinks
    Unique_inlinks =  models.FloatField(null=True)# Champ pour Unique Inlinks
    Unique_JS_inlinks = models.CharField(max_length=30, null=True) # Champ pour Unique JS Inlinks
    of_Total = models.FloatField(null=True)# Champ pour % of Tota
    Outlinks = models.FloatField(null=True)# Champ pour Outlinks
    Unique_Outlinks = models.FloatField(null=True)# Champ pour Unique Outlinks
    Unique_JS_Outlinks = models.CharField(max_length=30, null=True) # Champ pour Unique JS Outlinks
    External_Outlinks =  models.FloatField(null=True)# Champ pour External Outlinks
    Unique_External_Outlinks = models.FloatField(null=True)# Champ pour Unique External Outlinks
    Unique_External_JS_Outlinks = models.FloatField(null=True)# Champ pour Unique External JS Outlinks
    Closest_Similarity_Match = models.FloatField(null=True)# Champ pour Closest Similarity Match
    NoNear_Duplicates = models.FloatField(null=True)# Champ pour No. Near Duplicates 
    Spelling_Errors = models.FloatField(null=True)# Champ pour Spelling Errors 
    Grammar_Errors = models.FloatField(null=True)# Champ pour Grammar Errors
    Hash =  models.CharField(max_length=150, null=True) # Champ pour Hash
    Response_time = models.CharField(max_length=150, null=True) # Champ pour Response time
    Last_modified = models.CharField(max_length=150, null=True) # Champ pour Last Modified
    Redirect_URL = models.CharField(max_length=150, null=True) # Champ pour Redirect URL
    Redirect_type = models.CharField(max_length=150, null=True) # Champ pour Redirect Type
    Cookies = models.CharField(max_length=150, null=True) # Champ pour Cookies
    HTTP_Version = models.FloatField(null=True)# Champ pour HTTP Version
    URL_Encoded_Address = models.CharField(max_length=150, null=True)# Champ pour URL Encoded Address
    Crawl_Timestamp = models.CharField(max_length=350, null=True) # Champ pour Crawl Timestamp
    Errors = models.CharField(max_length=150, null=True) # Champ pour Errors
    Warnings = models.FloatField(null=True)# Champ pour Warnings
    Total_Types = models.FloatField(null=True) # Champ pour Total Types
    Unique_Types = models.CharField(max_length=150, null=True)  # Champ pour Unique Types
    Type_1 = models.FloatField(null=True)  # Champ pour Type-1
    Indexability_y = models.CharField(max_length=150, null=True) # Champ pour Indexability_y
    Indexability_Status_y =  models.CharField(max_length=150, null=True) # Champ pour Indexability Status_y
    Title1_score = models.FloatField(null=True)# Champ pour Title 1 score
    Meta_Description1_score = models.FloatField(null=True)  # Champ pour Meta Description 1 score
    Meta_Keywords1_score =  models.FloatField(null=True)  # Champ pour Meta Keywords 1 score
    H1_1_score = models.FloatField(null=True) # Champ pour H1-1 score
    H1_2_score= models.FloatField(null=True)  # Champ pour H1-2 score
    H2_1_score = models.FloatField(null=True)  # Champ pour H2-1 score
    H2_2_score = models.FloatField(null=True)  # Champ pour H2-2 score
    Meta_Robots_1_score = models.FloatField(null=True)  # Champ pour Meta Robots 1 score
    Url_Score = models.FloatField(null=True)  # Champ pour Url score

    class Meta:
        unique_together = ['Thekeyword', 'Url', 'Top10','Position', 'Http_code_babbar', 'Ttfb_babbar', 'Ttfb_babbar', 'Page_value_babbar',
                           'Page_trust_babbar', 'Semantic_value_babbar', 'Backlinks_babbar', 'Backlinks_host_babbar', 'Host_outlinks_babbar', 
                           'Outlinks_babbar', 'Desktop_first_contentful_paint_terrain', 'Desktop_first_input_delay_terain', 
                           'Desktop_largest_contentful_paint_terrain', 'Desktop_cumulative_layout_shift_terrain',
                           'Desktop_first_contentful_paint_lab', 'Desktop_speed_index_lab', 'Desktop_largest_contentful_paint_lab',
                           'Desktop_time_to_interactive_lab', 'Desktop_total_blocking_time_lab', 'Desktop_cumulative_layout_shift_lab',
                           'Mobile_first_contentful_paint_terrain', 'Mobile_first_input_delay_terain', 'Mobile_largest_contentful_paint_terrain',
                           'Mobile_cumulative_layout_shift_terrain', 'Mobile_first_contentful_paint_lab', 'Mobile_speed_index_lab', 
                           'Mobile_largest_contentful_paint_lab', 'Mobile_time_to_interactive_lab', 'Mobile_total_blocking_time_lab',
                           'Mobile_cumulative_layout_shift_lab', 'SOSEO_yourtext_guru', 'DSEO_yourtext_guru', 'Score_1fr', 'Content_type', 'Status_code',
                           'Status', 'Indexability_x', 'Indexability_status_x', 'Title1', 'Title1_length', 'Title1_pixel_width', 'Title2', 'Title2_length',
                           'Title2_pixel_width', 'Meta_description1', 'Meta_description1_length', 'Meta_description1_Pixel_width', 'Meta_description1_Pixel_width',
                           'Meta_description2', 'Meta_description2_length', 'Meta_description2_Pixel_width', 'Meta_description2_Pixel_width', 'Meta_description2_Pixel_width',
                           'Meta_Keywords1', 'Meta_keywords1_length', 'H1_1', 'H1_1_length', 'H1_2', 'H1_2_length', 'H2_1', 'H2_1_length', 'H2_2', 'H2_2_length', 'Meta_robots_1',
                           'Meta_robots_2', 'Meta_robots_3', 'X_robots_tag1', 'Meta_Refresh_1', 'Canonical_link_element1', 'Canonical_link_element2', 'rel_next_1', 'rel_prev_1',
                           'HTTP_rel_next_1', 'HTTP_rel_prev_1', 'amphtml_link_element', 'Size_bytes', 'Word_count', 'Sentence_Count', 'Average_words_per_sentence',
                           'Flesch_reading_ease_score', 'Readability', 'Text_ratio', 'Crawl_depth', 'Link_score', 'Inlinks', 'Unique_inlinks', 'Unique_JS_inlinks',
                           'of_Total', 'Outlinks', 'Unique_Outlinks', 'Unique_JS_Outlinks', 'External_Outlinks', 'Unique_External_Outlinks', 'Unique_External_JS_Outlinks',
                           'Closest_Similarity_Match', 'NoNear_Duplicates', 'Spelling_Errors', 'Grammar_Errors', 'Hash', 'Response_time', 'Last_modified', 'Redirect_URL',
                           'Redirect_type', 'Cookies', 'HTTP_Version', 'URL_Encoded_Address', 'Crawl_Timestamp','Errors', 'Warnings', 'Total_Types', 'Unique_Types', 'Type_1',
                           'Indexability_y', 'Indexability_Status_y', 'Title1_score', 'Meta_Description1_score', 'Meta_Description1_score', 'Meta_Keywords1_score',
                           'Meta_Keywords1_score', 'Meta_Keywords1_score', 'H1_1_score', 'H1_2_score', 'H2_1_score', 'H2_2_score', 'Meta_Robots_1_score', 'Url_Score']

User = get_user_model()

class Test(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    Keyword = models.CharField(max_length=250, null=True) #keyword
    nb_url =  models.FloatField(null=True) #nb_url
    precision =  models.FloatField(null=True) # précision
    Ttfb_babbar_score = models.FloatField(null=True) # Ttfb_babbar_score
    Page_value_babbar_score = models.FloatField(null=True) # Page_value_babbar_score
    Page_trust_babbar_score = models.FloatField(null=True) # Page_trust_babbar_score
    Semantic_value_babbar_score = models.FloatField(null=True) # Semantic_value_babbar_score
    Backlinks_babbar_score = models.FloatField(null=True) # Backlinks_babbar_score
    Backlinks_host_babbar_score = models.FloatField(null=True) # Backlinks_host_babbar_score
    Host_outlinks_babbar_score = models.FloatField(null=True) # Host_outlinks_babbar_score
    Outlinks_babbar_score = models.FloatField(null=True) # Outlinks_babbar_score
    Desktop_first_contentful_paint_terrain_score = models.FloatField(null=True) # Desktop_first_contentful_paint_terrain_score
    Desktop_first_input_delay_terain_score = models.FloatField(null=True) # Desktop_first_input_delay_terain_score
    Desktop_largest_contentful_paint_terrain_score = models.FloatField(null=True) # Desktop_largest_contentful_paint_terrain_score
    Desktop_cumulative_layout_shift_terrain_score = models.FloatField(null=True) # Desktop_cumulative_layout_shift_terrain_score
    Desktop_first_contentful_paint_lab_score = models.FloatField(null=True) # Desktop_first_contentful_paint_lab_score
    Desktop_speed_index_lab_score = models.FloatField(null=True) # Desktop_speed_index_lab_score
    Desktop_largest_contentful_paint_lab_score = models.FloatField(null=True) # Desktop_largest_contentful_paint_lab_score
    Desktop_time_to_interactive_lab_score = models.FloatField(null=True) # Desktop_time_to_interactive_lab_score
    Desktop_total_blocking_time_lab_score = models.FloatField(null=True) # Desktop_total_blocking_time_lab_score
    Desktop_cumulative_layout_shift_lab_score = models.FloatField(null=True) # Desktop_cumulative_layout_shift_lab_score
    Mobile_first_contentful_paint_terrain_score = models.FloatField(null=True) # Mobile_first_contentful_paint_terrain_score
    Mobile_first_input_delay_terain_score = models.FloatField(null=True) # Mobile_first_input_delay_terain_score
    Mobile_largest_contentful_paint_terrain_score = models.FloatField(null=True) # Mobile_largest_contentful_paint_terrain_score
    Mobile_cumulative_layout_shift_terrain_score = models.FloatField(null=True) # Mobile_cumulative_layout_shift_terrain_score
    Mobile_first_contentful_paint_lab_score = models.FloatField(null=True) # Mobile_first_contentful_paint_lab_score
    Mobile_speed_index_lab_score = models.FloatField(null=True) # Mobile_speed_index_lab_score
    Mobile_largest_contentful_paint_lab_score = models.FloatField(null=True) # Mobile_largest_contentful_paint_lab_score
    Mobile_time_to_interactive_lab_score = models.FloatField(null=True) # Mobile_time_to_interactive_lab_score
    Mobile_total_blocking_time_lab_score = models.FloatField(null=True) # Mobile_total_blocking_time_lab_score
    Mobile_cumulative_layout_shift_lab_score = models.FloatField(null=True) # Mobile_cumulative_layout_shift_lab_score
    SOSEO_yourtext_guru_score = models.FloatField(null=True) # SOSEO_yourtext_guru_score
    DSEO_yourtext_guru_score = models.FloatField(null=True) # DSEO_yourtext_guru_score
    Score_1fr_score = models.FloatField(null=True) # Score_1fr_score
    Title1_score = models.FloatField(null=True) # Title1_score
    Title1_length_score = models.FloatField(null=True) # Title1_length_score
    Title1_pixel_width_score = models.FloatField(null=True) # Title1_pixel_width_score
    Title2_score = models.FloatField(null=True) # Title2_score
    Title2_length_score = models.FloatField(null=True) # Title2_length_score
    Title2_pixel_width_score = models.FloatField(null=True) # Title2_pixel_width_score
    Meta_description1_score = models.FloatField(null=True) # Meta_description1_score
    Meta_description1_length_score = models.FloatField(null=True) # Meta_description1_length_score
    Meta_description1_Pixel_width_score = models.FloatField(null=True) # Meta_description1_Pixel_width_score
    Meta_description2_score = models.FloatField(null=True) #  Meta_description2_score
    Meta_description2_length_score = models.FloatField(null=True) # Meta_description2_length_score
    Meta_description2_Pixel_width_score = models.FloatField(null=True) # Meta_description2_Pixel_width_score
    Meta_Keywords1_score = models.FloatField(null=True) # Meta_Keywords1_score
    Meta_keywords1_length_score = models.FloatField(null=True) # Meta_keywords1_length_score
    H1_1_score = models.FloatField(null=True) # H1_1_score
    H1_1_length_score = models.FloatField(null=True) # H1_1_length_score
    H1_2_score = models.FloatField(null=True) # H1_2_score
    H1_2_length_score = models.FloatField(null=True) # H1_2_length_score
    H2_1_score = models.FloatField(null=True) # H2_1_score
    H2_1_length_score = models.FloatField(null=True) # H2_1_length_score
    H2_2_score = models.FloatField(null=True) # H2_2_score
    H2_2_length_score = models.FloatField(null=True) # H2_2_length_score
    Meta_robots_1_score = models.FloatField(null=True) # Meta_robots_1_score
    Meta_robots_2_score = models.FloatField(null=True) # Meta_robots_2_score
    Meta_robots_3_score = models.FloatField(null=True) # Meta_robots_3_score
    Canonical_link_element2_score = models.FloatField(null=True) # Canonical_link_element2_score
    Size_bytes_score = models.FloatField(null=True) # Size_bytes_score
    Word_count_score = models.FloatField(null=True) # Word_count_score
    Sentence_Count_score = models.FloatField(null=True) # Sentence_Count_score
    Average_words_per_sentence_score = models.FloatField(null=True) # Average_words_per_sentence_score
    Flesch_reading_ease_score_score = models.FloatField(null=True) # Flesch_reading_ease_score_score
    Text_ratio_score = models.FloatField(null=True) # Text_ratio_score
    Crawl_depth_score = models.FloatField(null=True) # Crawl_depth_score
    Inlinks_score = models.FloatField(null=True) # Inlinks_score
    Unique_inlinks_score = models.FloatField(null=True) # Unique_inlinks_score
    Unique_JS_inlinks_score = models.FloatField(null=True) # Unique_JS_inlinks_score
    of_Total_score = models.FloatField(null=True) # of_Total_score
    Outlinks_score = models.FloatField(null=True) # Outlinks_score
    Unique_Outlinks_score = models.FloatField(null=True) # Unique_Outlinks_score
    Unique_JS_Outlinks_score = models.FloatField(null=True) # Unique_JS_Outlinks_score
    External_Outlinks_score = models.FloatField(null=True) # External_Outlinks_score
    Unique_External_Outlinks_score = models.FloatField(null=True) # Unique_External_Outlinks_score
    Unique_External_JS_Outlinks_score = models.FloatField(null=True) # Unique_External_JS_Outlinks_score
    Response_time_score = models.FloatField(null=True) # Response_time_score
    Errors_score = models.FloatField(null=True) # Errors_score
    Warnings_score = models.FloatField(null=True) # Warnings_score
    Total_Types_score = models.FloatField(null=True) # Total_Types_score
    Unique_Types_score = models.FloatField(null=True) # Unique_Types_score
    Title1_score_score = models.FloatField(null=True) # Title1_score_score
    Meta_Description1_score_score = models.FloatField(null=True) # Meta_Description1_score_score
    Meta_Keywords1_score_score = models.FloatField(null=True) # Meta_Keywords1_score_score
    H1_1_score_score = models.FloatField(null=True) # H1_1_score_score
    H1_2_score_score = models.FloatField(null=True) # H1_2_score_score
    H2_1_score_score = models.FloatField(null=True) # H2_1_score_score
    H2_2_score_score = models.FloatField(null=True) # H2_2_score_score
    date_test = models.DateField(null=True)

class Data_Url(models.Model):
    
    Thekeyword = models.CharField(max_length=150, null=True)  # Champ pour Keyword
    #Position = models.PositiveIntegerField(null=True)  # Champ pour la position
    Url = models.CharField(max_length=200, null=True)  # Champ pour l'URL
    Top10 = models.BooleanField(null=True)  # Champ pour Top 10 (0 ou 1)
    Http_code_babbar = models.FloatField(null=True)  # Champ pour HTTP Code BABBAR
    Ttfb_babbar = models.FloatField(null=True)  # Champ pour TTFB BABBAR (en ms) 
    Page_value_babbar = models.FloatField(null=True)  # Champ pour Page Value BABBAR
    Page_trust_babbar = models.FloatField(null=True) # Champ pour Page Trust BABBAR
    Semantic_value_babbar = models.FloatField(null=True)# Champ pour Semantic Value BABBAR
    Backlinks_babbar = models.FloatField(null=True)  # Champ pour Backlinks BABBAR
    Backlinks_host_babbar = models.FloatField(null=True)  # Champ pour Backlinks Host BABBAR
    Host_outlinks_babbar = models.FloatField(null=True)  # Champ pour Host Outlinks BABBAR
    Outlinks_babbar = models.FloatField(null=True)  # Champ pour Outlinks BABBAR
    Desktop_first_contentful_paint_terrain = models.FloatField(null=True,  blank=True) # Champ pour Desktop First Contentful Paint Terrain
    Desktop_first_input_delay_terain = models.FloatField(null=True, blank= True) # Champ pour Desktop First Input delay Terain
    Desktop_largest_contentful_paint_terrain = models.FloatField(null=True, blank= True) # Champ pour Desktop Largest Contentful Paint Terrain
    Desktop_cumulative_layout_shift_terrain = models.FloatField(null=True, blank= True) # Champ pour Desktop Cumulative Layout Shift Terrain
    Desktop_first_contentful_paint_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop First Contentful Paint Lab
    Desktop_speed_index_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop Speed Index Lab
    Desktop_largest_contentful_paint_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop Largest Contentful Paint Lab
    Desktop_time_to_interactive_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop Time to Interactive Lab
    Desktop_total_blocking_time_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop Total Blocking Time Lab
    Desktop_cumulative_layout_shift_lab = models.FloatField(null=True, blank=True) # Champ pour Desktop Cumulative Layout Shift Lab
    Mobile_first_contentful_paint_terrain =  models.FloatField(null=True, blank=True) # Champ pour Mobile Contentful Paint Terrain
    Mobile_first_input_delay_terain = models.FloatField(null=True) # Champ pour Mobile First Input Delay Terain
    Mobile_largest_contentful_paint_terrain =  models.FloatField(null=True) # Champ pour Mobile Largest Contentful Paint Terrain
    Mobile_cumulative_layout_shift_terrain = models.FloatField(null=True) # Champ pour Mobile Cumulative Layout Shift Terrain 
    Mobile_first_contentful_paint_lab = models.FloatField(null=True) # Champ pour Mobile First Contentful Paint Lab
    Mobile_speed_index_lab = models.FloatField(null=True) # Champ pour Mobile Speed Index Lab
    Mobile_largest_contentful_paint_lab = models.FloatField(null=True) # Champ pour Mobile Largest Contentful Paint Lab
    Mobile_time_to_interactive_lab = models.FloatField(null=True) # Champ pour Mobile Time to Interactive Lab
    Mobile_total_blocking_time_lab = models.FloatField(null=True) # Champ pour Mobile Total Blocking Time Lab
    Mobile_cumulative_layout_shift_lab = models.FloatField(null=True) # Champ pour Mobile Cumulative Layout Shift Lab
    SOSEO_yourtext_guru = models.FloatField(null=True)# Champ pour SOSEO yourtext_guru
    DSEO_yourtext_guru = models.FloatField(null=True)# Champ pour DSEO yourtext_guru
    Score_1fr = models.FloatField(null=True) # Champ pour Score_1fr
    Content_type = models.CharField(max_length=150, null=True)  # Champ pour Content Type
    Status_code = models.CharField(max_length=150, null=True)  # Champ pour Status Code
    Status = models.CharField(max_length=150, null=True)  # Champ pour Status
    Indexability_x =  models.CharField(max_length=150, null=True)  # Champ pour Indexability_x
    Indexability_status_x = models.CharField(max_length=150, null=True)  # Champ pour Indexability Status_x
    Title1 = models.CharField(max_length=350, null=True)  # Champ pour Title 1
    Title1_length = models.CharField(max_length=350, null=True)  # Champ pour Title 1 Length
    Title1_pixel_width = models.CharField(max_length=150, null=True) # Champ pour Title 1 Pixel Width
    Title2 = models.CharField(max_length=150, null=True) # Champ pour Title 2
    Title2_length = models.CharField(max_length=150, null=True)  # Champ pour Title 2 Length
    Title2_pixel_width = models.CharField(max_length=150, null=True) # Champ pour Title 2 Pixel Width
    Meta_description1 = models.CharField(max_length=150, null=True) # Champ pour Meta Description 1
    Meta_description1_length =  models.CharField(max_length=350, null=True) # Champ pour Meta Description 1 Length
    Meta_description1_Pixel_width =  models.CharField(max_length=350, null=True) # Champ pour Meta Description 1 Pixel Width
    Meta_description2 = models.CharField(max_length=150, null=True) # Champ pour Meta Description 2
    Meta_description2_length =  models.CharField(max_length=350, null=True) # Champ pour Meta Description 2 Length
    Meta_description2_Pixel_width =  models.CharField(max_length=350, null=True) # Champ pour Meta Description 2 Pixel Width
    Meta_Keywords1 = models.CharField(max_length=350, null=True) # Champ pour Meta Keywords 1
    Meta_keywords1_length = models.CharField(max_length=350, null=True) # Champ pour Meta Keywords 1 Length
    H1_1  = models.CharField(max_length=150, null=True) # Champ pour H1-1
    H1_1_length = models.CharField(max_length=350, null=True) # Champ pour H1-1 Length
    H1_2 = models.CharField(max_length=150, null=True) # Champ pour H1-2
    H1_2_length = models.CharField(max_length=150, null=True) # Champ pour H1-2 Length
    H2_1 = models.CharField(max_length=350, null=True) # Champ pour H2-1
    H2_1_length = models.CharField(max_length=350, null=True) # Champ pour H2-1 Length
    H2_2 = models.CharField(max_length=150, null=True) # Champ pour H2-2 
    H2_2_length = models.CharField(max_length=350, null=True) # Champ pour H2-2 Length
    Meta_robots_1 = models.CharField(max_length=150, null=True) # Champ pour Meta Robots 1
    Meta_robots_2 = models.CharField(max_length=150, null=True) # Champ pour Meta Robots 2
    Meta_robots_3 = models.CharField(max_length=150, null=True) # Champ pour Meta Robots 3                                                           
    X_robots_tag1 = models.CharField(max_length=150, null=True) # Champ pour X-Robots-Tag 1
    Meta_Refresh_1 = models.CharField(max_length=150, null=True) # Champ pour Meta Refresh 1
    Canonical_link_element1 = models.CharField(max_length=350, null=True) # Champ pour Canonical Link Element 1
    Canonical_link_element2 = models.CharField(max_length=350, null=True) # Champ pour Canonical Link Element 2
    rel_next_1 = models.CharField(max_length=350, null=True) # Champ pour rel="next" 1
    rel_prev_1 = models.CharField(max_length=350, null=True) # Champ pour rel="prev" 1
    HTTP_rel_next_1 = models.CharField(max_length=350, null=True) # Champ pour HTTP rel="next" 1
    HTTP_rel_prev_1 = models.CharField(max_length=150, null=True) # Champ pour HTTP rel="prev" 1
    amphtml_link_element = models.CharField(max_length=150, null=True) # Champ pour amphtml Link Element
    Size_bytes = models.FloatField(null=True)# Champ pour Size (bytes)
    Word_count = models.FloatField(null=True)# Champ pour Word Count
    Sentence_Count = models.FloatField(null=True)# Champ pour sentence Count
    Average_words_per_sentence = models.CharField(max_length=150, null=True) # Champ pour Average Words Per Sentence
    Flesch_reading_ease_score = models.FloatField(null=True)# Champ pour Flesch Reading Ease Score
    Readability = models.CharField(max_length=30, null=True) # Champ pour Readability
    Text_ratio = models.CharField(max_length=30, null=True) # Champ pour Text Ratio
    Crawl_depth = models.FloatField(null=True)# Champ pour Crawl Depth
    Link_score = models.FloatField(null=True)# Champ pour Link Score
    Inlinks =  models.FloatField(null=True)# Champ pour Inlinks
    Unique_inlinks =  models.FloatField(null=True)# Champ pour Unique Inlinks
    Unique_JS_inlinks = models.CharField(max_length=30, null=True) # Champ pour Unique JS Inlinks
    of_Total = models.FloatField(null=True)# Champ pour % of Tota
    Outlinks = models.FloatField(null=True)# Champ pour Outlinks
    Unique_Outlinks = models.FloatField(null=True)# Champ pour Unique Outlinks
    Unique_JS_Outlinks = models.CharField(max_length=30, null=True) # Champ pour Unique JS Outlinks
    External_Outlinks =  models.FloatField(null=True)# Champ pour External Outlinks
    Unique_External_Outlinks = models.FloatField(null=True)# Champ pour Unique External Outlinks
    Unique_External_JS_Outlinks = models.FloatField(null=True)# Champ pour Unique External JS Outlinks
    Closest_Similarity_Match = models.FloatField(null=True)# Champ pour Closest Similarity Match
    NoNear_Duplicates = models.FloatField(null=True)# Champ pour No. Near Duplicates 
    Spelling_Errors = models.FloatField(null=True)# Champ pour Spelling Errors 
    Grammar_Errors = models.FloatField(null=True)# Champ pour Grammar Errors
    Hash =  models.CharField(max_length=150, null=True) # Champ pour Hash
    Response_time = models.CharField(max_length=150, null=True) # Champ pour Response time
    Last_modified = models.CharField(max_length=150, null=True) # Champ pour Last Modified
    Redirect_URL = models.CharField(max_length=150, null=True) # Champ pour Redirect URL
    Redirect_type = models.CharField(max_length=150, null=True) # Champ pour Redirect Type
    Cookies = models.CharField(max_length=150, null=True) # Champ pour Cookies
    HTTP_Version = models.FloatField(null=True)# Champ pour HTTP Version
    URL_Encoded_Address = models.CharField(max_length=150, null=True)# Champ pour URL Encoded Address
    Crawl_Timestamp = models.CharField(max_length=350, null=True) # Champ pour Crawl Timestamp
    Errors = models.CharField(max_length=150, null=True) # Champ pour Errors
    Warnings = models.FloatField(null=True)# Champ pour Warnings
    Total_Types = models.FloatField(null=True) # Champ pour Total Types
    Unique_Types = models.CharField(max_length=150, null=True)  # Champ pour Unique Types
    Type_1 = models.FloatField(null=True)  # Champ pour Type-1
    Indexability_y = models.CharField(max_length=150, null=True) # Champ pour Indexability_y
    Indexability_Status_y =  models.CharField(max_length=150, null=True) # Champ pour Indexability Status_y
    Title1_score = models.FloatField(null=True)# Champ pour Title 1 score
    Meta_Description1_score = models.FloatField(null=True)  # Champ pour Meta Description 1 score
    Meta_Keywords1_score =  models.FloatField(null=True)  # Champ pour Meta Keywords 1 score
    H1_1_score = models.FloatField(null=True) # Champ pour H1-1 score
    H1_2_score= models.FloatField(null=True)  # Champ pour H1-2 score
    H2_1_score = models.FloatField(null=True)  # Champ pour H2-1 score
    H2_2_score = models.FloatField(null=True)  # Champ pour H2-2 score
    Meta_Robots_1_score = models.FloatField(null=True)  # Champ pour Meta Robots 1 score
    Date_added = models.DateField(null=True, blank=True)
    Url_Score = models.FloatField(null=True)  # Champ pour Url score    

    

class Keyword_Url(models.Model):
    Keyword_url = models.CharField(max_length=255, null=True)


class MinMaxValue(models.Model):
    test_instance = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='min_max_values')
    attribute_name = models.CharField(max_length=255)
    attribute_value = models.FloatField(null=True)
    min_max = models.CharField(max_length=50)
    



    




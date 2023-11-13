# SEO_Prediction_App/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # Ajoutez des champs personnalisés si nécessaire
   
    # Spécifiez des noms de relation inverses personnalisés pour éviter les conflits
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)
  

class Keyword(models.Model):
    Keyword = models.CharField(max_length=255, null=True)


class Data(models.Model):
    keyword = models.CharField(max_length=2150, null=True)  # Champ pour Keyword
    Position = models.PositiveIntegerField(null=True)  # Champ pour la position
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
    Desktop_first_contentful_paint_terrain = models.FloatField(null=True) # Champ pour Desktop First Contentful Paint Terrain
    Desktop_first_input_delay_terain = models.FloatField(null=True) # Champ pour Desktop First Input delay Terain
    Desktop_largest_contentful_paint_terrain = models.FloatField(null=True) # Champ pour Desktop Largest Contentful Paint Terrain
    Desktop_cumulative_layout_shift_terrain = models.FloatField(null=True) # Champ pour Desktop Cumulative Layout Shift Terrain
    Desktop_first_contentful_paint_lab = models.FloatField(null=True) # Champ pour Desktop First Contentful Paint Lab
    Desktop_speed_index_lab = models.FloatField(null=True) # Champ pour Desktop Speed Index Lab
    Desktop_largest_contentful_paint_lab = models.FloatField(null=True) # Champ pour Desktop Largest Contentful Paint Lab
    Desktop_time_to_interactive_lab = models.FloatField(null=True) # Champ pour Desktop Time to Interactive Lab
    Desktop_total_blocking_time_lab = models.FloatField(null=True) # Champ pour Desktop Total Blocking Time Lab
    Desktop_cumulative_layout_shift_lab = models.FloatField(null=True) # Champ pour Desktop Cumulative Layout Shift Lab
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
    Sentence_Count = models.FloatField(null=True)# Champ pour sentece Count
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
    Url_score = models.FloatField(null=True)  # Champ pour Url score
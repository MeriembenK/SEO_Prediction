import os
import time
import pandas as pd
import django
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
django.setup()
from SEO_Prediction_App.models import Data, Keyword

data_sets_directory = './DataSets'



def process_column(value):
   
    if isinstance(value, tuple) and len(value) > 0:
        value = value[0]

    if value:
        value = float(value)
    else:
        value = 0

    return value


# Importez d'abord les mots-clés
def import_keywords_from_csv(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            csv_path = os.path.join(directory_path, filename)
            df = pd.read_csv(csv_path)
 
            keyword_name = os.path.splitext(filename)[0]

            keyword, _ = Keyword.objects.get_or_create(Keyword=keyword_name)
            # Si le Keyword existait déjà, vous pouvez mettre à jour d'autres attributs si nécessaire


# Importez ensuite les données associées à chaque mot-clé
def import_data_from_csv_files(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            csv_path = os.path.join(directory_path, filename)
            df = pd.read_csv(csv_path)
        
            for _, row in df.iterrows():

                
                keyword_name = os.path.splitext(filename)[0]
                Thekeyword = Keyword.objects.get(Keyword=keyword_name)
                dseo_yourtext_guru_value = row.get('DSEO yourtext_guru', '')
                Score_1fr_value = row.get('Score_1fr', ''),
                h1_2_score_value = row.get('H1-2 score', ''),
                mobile_cumulative_layout_shift_lab_value = row.get('Mobile Speed Index Lab', ''),
                mobile_cumulative_layout_shift_terrain_value = row.get('Mobile Cumulative Layout Shift Terrain', ''),
                mobile_first_contentful_paint_lab_value = row.get('Mobile First Contentful Paint Lab', ''),
                mobile_first_contentful_paint_terrain_value = row.get('Mobile First Contentful Paint Terrain', ''),
                mobile_first_input_delay_terain_value = row.get('Mobile First Input Delay Terain', ''),
                mobile_largest_contentful_paint_lab_value = row.get('Mobile Largest Contentful Paint Lab', ''),
                mobile_largest_contentful_paint_terrain_value = row.get('Mobile Largest Contentful Paint Terrain', ''),
                mobile_speed_index_lab_value = row.get('Mobile Speed Index Lab', ''),
                mobile_time_to_interactive_lab_value = row.get('Mobile Time to Interactive Lab', ''),
                mobile_total_blocking_time_lab_value = row.get('Mobile Total Blocking Time Lab', ''),
                soseo_yourtext_guru_value = row.get('SOSEO yourtext_guru', ''),
                desktop_first_contentful_paint_terrain_value = row.get('Desktop First Contentful Paint Terrain', ''),
                desktop_first_input_delay_terain_value=row.get('Desktop First Input Delay Terain', ''),
                desktop_largest_contentful_paint_terrain_value=row.get('Desktop Largest Contentful Paint Terrain', ''),
                desktop_cumulative_layout_shift_terrain_vlaue= row.get('Desktop Cumulative Layout Shift Terrain', ''),
                desktop_first_contentful_paint_lab_value= row.get('Desktop First Contentful Paint Lab', ''),
                desktop_speed_index_lab_value= row.get('Desktop Speed Index Lab', ''),
                desktop_largest_contentful_paint_lab_value = row.get('Desktop Largest Contentful Paint Lab', ''),
                desktop_time_to_interactive_lab_value = row.get('Desktop Time to Interactive Lab', ''),
                desktop_cumulative_layout_shift_lab_value = row.get('Desktop Cumulative Layout Shift Lab', ''),
                desktop_total_blocking_time_lab_value = row.get('Desktop Total Blocking Time Lab', ''),
                Http_code_babbar_value =row.get('HTTP code BABBAR', ''),
                Ttfb_babbar_value=row.get('TTFB (en ms) BABBAR', ''),
                Page_value_babbar_value=row.get('Page Value BABBAR', ''),
                Page_trust_babbar_value=row.get('Page Trust BABBAR', ''),
                Semantic_value_babbar_value=row.get('Semantic Value BABBAR', ''),
                Backlinks_babbar_value=row.get('Backlinks BABBAR', ''),       
                Backlinks_host_babbar_value=row.get('Backlinks host BABBAR', ''),
                Host_outlinks_babbar_value=row.get('Host Outlinks BABBAR', ''),
                Outlinks_babbar_value=row.get('Outlinks BABBAR', ''),            
                Type_1_value= row.get('Type 1', ''), 
                
                
                data = Data(
                    Thekeyword=row.get('Keyword', ''),
                    Url=row.get('Url', ''),
                    Top10 = row.get('Top10', ''),
                    Position=row.get('Position', ''),
                    Http_code_babbar= process_column(Http_code_babbar_value),
                    Ttfb_babbar=process_column(Ttfb_babbar_value),                   
                    Page_value_babbar=process_column(Page_value_babbar_value),
                    Page_trust_babbar=process_column(Page_trust_babbar_value),
                    Semantic_value_babbar=process_column(Semantic_value_babbar_value),
                    Backlinks_babbar=process_column(Backlinks_babbar_value),       
                    Backlinks_host_babbar=process_column(Backlinks_host_babbar_value),
                    Host_outlinks_babbar=process_column(Host_outlinks_babbar_value),
                    Outlinks_babbar= process_column(Outlinks_babbar_value),
                    Desktop_first_contentful_paint_terrain=process_column(desktop_first_contentful_paint_terrain_value),
                    Desktop_first_input_delay_terain=process_column(desktop_first_input_delay_terain_value),
                    Desktop_largest_contentful_paint_terrain=process_column(desktop_largest_contentful_paint_terrain_value),
                    Desktop_cumulative_layout_shift_terrain= process_column(desktop_cumulative_layout_shift_terrain_vlaue),
                    Desktop_first_contentful_paint_lab= process_column(desktop_first_contentful_paint_lab_value),
                    Desktop_speed_index_lab= process_column(desktop_speed_index_lab_value),
                    Desktop_total_blocking_time_lab = process_column(desktop_total_blocking_time_lab_value),
                    Desktop_largest_contentful_paint_lab = process_column(desktop_largest_contentful_paint_lab_value),
                    Desktop_time_to_interactive_lab = process_column(desktop_time_to_interactive_lab_value),
                    Desktop_cumulative_layout_shift_lab = process_column(desktop_cumulative_layout_shift_lab_value),
                    Mobile_first_contentful_paint_terrain = process_column(mobile_first_contentful_paint_terrain_value),
                    Mobile_first_input_delay_terain = process_column(mobile_first_input_delay_terain_value),
                    Mobile_largest_contentful_paint_terrain = process_column(mobile_largest_contentful_paint_terrain_value),
                    Mobile_cumulative_layout_shift_terrain = process_column(mobile_cumulative_layout_shift_terrain_value),
                    Mobile_first_contentful_paint_lab = process_column(mobile_first_contentful_paint_lab_value),
                    Mobile_speed_index_lab = process_column(mobile_speed_index_lab_value),
                    Mobile_largest_contentful_paint_lab = process_column(mobile_largest_contentful_paint_lab_value),
                    Mobile_time_to_interactive_lab = process_column(mobile_time_to_interactive_lab_value),
                    Mobile_total_blocking_time_lab = process_column(mobile_total_blocking_time_lab_value),
                    Mobile_cumulative_layout_shift_lab =  process_column(mobile_cumulative_layout_shift_lab_value),
                    SOSEO_yourtext_guru = process_column(soseo_yourtext_guru_value),
                    DSEO_yourtext_guru= process_column(dseo_yourtext_guru_value),
                    Score_1fr = process_column(Score_1fr_value),
                    Content_type = row.get('Content Type', ''),
                    Status_code = row.get('Status Code', ''),
                    Status = row.get('Status', ''),
                    Indexability_x = row.get('Indexability_x', ''),
                    Indexability_status_x = row.get('Indexability Status_x', ''),
                    Title1 = row.get('Title 1', ''),
                    Title1_length = row.get('Title 1 Length', ''),
                    Title1_pixel_width = row.get('Title 1 Pixel Width', ''),
                    Title2 = row.get('Title 2', ''),
                    Title2_length = row.get('Title 2 Length', ''),
                    Title2_pixel_width = row.get('Title 2 Pixel Width', ''),
                    Meta_description1 = row.get('Meta Description 1', ''),
                    Meta_description1_length = row.get('Meta Description 1 Length', ''),
                    Meta_description1_Pixel_width = row.get('Meta Description 1 Pixel Width', ''),
                    Meta_description2 = row.get('Meta Description 2', ''), 
                    Meta_description2_length = row.get('Meta Description 2 Length', ''),
                    Meta_description2_Pixel_width = row.get('Meta Description 2 Pixel Width', ''),
                    Meta_Keywords1 = row.get('Meta Keywords 1', ''),
                    Meta_keywords1_length = row.get('Meta Keywords 1 Length', ''),
                    H1_1 = row.get('H1-1', ''),
                    H1_1_length = row.get('H1-1 Length', ''),
                    H1_2 = row.get('H1-2', ''),
                    H1_2_length = row.get('H1-2 Length', ''),
                    H2_1 = row.get('H2-1', ''),
                    H2_1_length = row.get('H2-1 Length', ''),
                    H2_2 = row.get('H2-2', ''),
                    H2_2_length = row.get('H2-2 Length', ''),
                    Meta_robots_1 = row.get('Meta Robots 1', ''),
                    Meta_robots_2 = row.get('Meta Robots 2', ''),
                    Meta_robots_3 = row.get('Meta Robots 3', ''),
                    X_robots_tag1 = row.get('X-Robots-Tag 1', ''),
                    Meta_Refresh_1 = row.get('Meta Refresh 1', ''),
                    Canonical_link_element1 = row.get('Canonical Link Element 1', ''),
                    Canonical_link_element2 = row.get('Canonical Link Element 2', ''),
                    rel_next_1 = row.get('rel="next" 1', ''),
                    rel_prev_1 = row.get('rel="prev" 1', ''),
                    HTTP_rel_next_1 = row.get('HTTP rel="next" 1', ''),
                    HTTP_rel_prev_1 = row.get('HTTP rel="prev" 1', ''),
                    amphtml_link_element = row.get('amphtml Link Element', ''),
                    Size_bytes = row.get('Size (bytes)', ''),
                    Word_count = row.get('Word Count', ''),
                    Sentence_Count = row.get('Sentence Count', ''),
                    Average_words_per_sentence = row.get('Average Words Per Sentence', ''),
                    Flesch_reading_ease_score = row.get('Flesch Reading Ease Score', ''),
                    Readability = row.get('Readabilit', ''),
                    Text_ratio = row.get('Text Ratio', ''),
                    Crawl_depth = row.get('Crawl Depth', ''),
                    Link_score = row.get('Link Score', ''),
                    Inlinks = row.get('Inlinks', ''),
                    Unique_inlinks = row.get('Unique Inlinks', ''),
                    Unique_JS_inlinks = row.get('Unique JS Inlinks', ''),
                    of_Total = row.get('% of Total', ''),
                    Outlinks = row.get('Outlinks', ''),
                    Unique_Outlinks = row.get('Unique Outlinks', ''),
                    Unique_JS_Outlinks = row.get('Unique JS Outlinks', ''),
                    External_Outlinks = row.get('External Outlinks', ''),
                    Unique_External_Outlinks = row.get('Unique External Outlinks', ''),
                    Unique_External_JS_Outlinks = row.get('Unique External JS Outlinks', ''),
                    Closest_Similarity_Match = row.get('Closest Similarity Match', ''),
                    NoNear_Duplicates = row.get('No. Near Duplicates', ''),
                    Spelling_Errors = row.get('Spelling Errors', ''),
                    Grammar_Errors = row.get('Grammar Errors', ''),
                    Hash = row.get('Hash', ''),
                    Response_time = row.get('Response Time', ''),
                    Last_modified = row.get('Last Modified', ''),
                    Redirect_URL = row.get('Redirect URL', ''),
                    Redirect_type = row.get('Redirect Type', ''),
                    Cookies = row.get('Cookies', ''),
                    HTTP_Version = row.get('HTTP Version', ''),
                    URL_Encoded_Address = row.get('URL Encoded Address', ''),
                    Crawl_Timestamp = row.get('Crawl Timestamp', ''),
                    Errors = row.get('Errors', ''),
                    Warnings = row.get('Warnings', ''),
                    Total_Types = row.get('Total Types', ''),
                    Unique_Types = row.get('Unique Types', ''),
                    Type_1 = process_column(Type_1_value),
                    Indexability_y = row.get('Indexability_y', ''),
                    Indexability_Status_y = row.get('Indexability Status_y', ''),
                    Title1_score = row.get('Title 1 score', ''),
                    Meta_Description1_score = row.get('Meta Description 1 score', ''),
                    Meta_Keywords1_score = row.get('Meta Keywords 1 score', ''),
                    H1_1_score = row.get('H1-1 score', ''),
                    H1_2_score = process_column(h1_2_score_value),
                    H2_1_score = row.get('H2-1 score', ''),
                    H2_2_score = row.get('H2-2 score', ''),
                    Meta_Robots_1_score = row.get('Meta Robots 1 score', ''),
                    Url_Score = row.get('Url score', ''),     
                    Date_added=datetime.now()

                 )
                  
                data.save()  # Enregistrez l'objet Data dans la base de données

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".csv"):
            print(f"Modification détectée dans le fichier: {event.src_path}")
            try:
                import_keywords_from_csv(data_sets_directory)
                import_data_from_csv_files(data_sets_directory)
            except pd.errors.EmptyDataError:
                print(f"Le fichier {event.src_path} est vide ou ne contient pas de colonnes.")
            except Exception as e:
                print(f"Erreur lors de la mise à jour des données : {e}")



if __name__ == "__main__":
   
     event_handler = MyHandler()
     observer = Observer()
     observer.schedule(event_handler, path=data_sets_directory, recursive=False)
     observer.start()

     try:
        while True:
            time.sleep(1) 
     except KeyboardInterrupt:
        observer.stop()
     observer.join()

# Delete all objects in the Data and Keyword models
"""Data.objects.all().delete()
Keyword.objects.all().delete()

print("All data and keywords have been deleted.")"""
  
data_count = Data.objects.count()
keyword_count = Keyword.objects.count()

print(f"Nombre de données (Data) dans la base de données : {data_count}")
print(f"Nombre de mots-clés (Keyword) dans la base de données : {keyword_count}")
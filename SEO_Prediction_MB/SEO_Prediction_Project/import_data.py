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

                if isinstance(Score_1fr_value, tuple) and len(Score_1fr_value) > 0:
                   Score_1fr_value = Score_1fr_value[0]
                if Score_1fr_value:
                   Score_1fr_value = float(Score_1fr_value)
                else:
                    Score_1fr_value = None

                if isinstance(dseo_yourtext_guru_value, tuple) and len(dseo_yourtext_guru_value) > 0:
                   dseo_yourtext_guru_value = dseo_yourtext_guru_value[0]
                if dseo_yourtext_guru_value:
                   dseo_yourtext_guru_value = float(dseo_yourtext_guru_value)
                else:
                    dseo_yourtext_guru_value = None

                # H1-2 score   
                if isinstance(h1_2_score_value, tuple) and len(h1_2_score_value) > 0:
                   h1_2_score_value = h1_2_score_value[0]
                if h1_2_score_value:
                   h1_2_score_value = float(h1_2_score_value)
                else:
                    h1_2_score_value = None   
               
                # Mobile_cumulative_layout_shift_lab
                if isinstance(mobile_cumulative_layout_shift_lab_value, tuple) and len(mobile_cumulative_layout_shift_lab_value) > 0:
                    mobile_cumulative_layout_shift_lab_value = mobile_cumulative_layout_shift_lab_value[0]
                if mobile_cumulative_layout_shift_lab_value:
                    mobile_cumulative_layout_shift_lab_value = float(mobile_cumulative_layout_shift_lab_value)
                else:
                    mobile_cumulative_layout_shift_lab_value = None   

                # Mobile_cumulative_layout_shift_terrain
                if isinstance(mobile_cumulative_layout_shift_terrain_value, tuple) and len(mobile_cumulative_layout_shift_terrain_value) > 0:
                    mobile_cumulative_layout_shift_terrain_value = mobile_cumulative_layout_shift_terrain_value[0]
                if mobile_cumulative_layout_shift_terrain_value:
                    mobile_cumulative_layout_shift_terrain_value = float(mobile_cumulative_layout_shift_terrain_value)
                else:
                    mobile_cumulative_layout_shift_terrain_value = None  
            

                # Mobile_first_contentful_paint_lab
                if isinstance(mobile_first_contentful_paint_lab_value, tuple) and len(mobile_first_contentful_paint_lab_value) > 0:
                    mobile_first_contentful_paint_lab_value = mobile_first_contentful_paint_lab_value[0]
                if mobile_first_contentful_paint_lab_value:
                    mobile_first_contentful_paint_lab_value = float(mobile_first_contentful_paint_lab_value)
                else:
                    mobile_first_contentful_paint_lab_value = None  

                   # Mobile_first_contentful_paint_terrain 
                if isinstance(mobile_first_contentful_paint_terrain_value, tuple) and len(mobile_first_contentful_paint_terrain_value) > 0:
                    mobile_first_contentful_paint_terrain_value = mobile_first_contentful_paint_terrain_value[0]
                if mobile_first_contentful_paint_terrain_value:
                    mobile_first_contentful_paint_terrain_value = float(mobile_first_contentful_paint_terrain_value)
                else:
                    mobile_first_contentful_paint_terrain_value = None  

                  # Mobile_first_input_delay_terain
                if isinstance(mobile_first_input_delay_terain_value, tuple) and len(mobile_first_input_delay_terain_value) > 0:
                   mobile_first_input_delay_terain_value = mobile_first_input_delay_terain_value[0]
                if mobile_first_input_delay_terain_value:
                   mobile_first_input_delay_terain_value = float(mobile_first_input_delay_terain_value)
                else:
                   mobile_first_input_delay_terain_value = None  

                # mobile_largest_contentful_paint_lab_value
                if isinstance(mobile_largest_contentful_paint_lab_value, tuple) and len(mobile_largest_contentful_paint_lab_value) > 0:
                    mobile_largest_contentful_paint_lab_value = mobile_largest_contentful_paint_lab_value[0]
                if mobile_largest_contentful_paint_lab_value:
                    mobile_largest_contentful_paint_lab_value = float(mobile_largest_contentful_paint_lab_value)
                else:
                    mobile_largest_contentful_paint_lab_value= None 

                # Mobile_largest_contentful_paint_terrain
                if isinstance(mobile_largest_contentful_paint_terrain_value, tuple) and len(mobile_largest_contentful_paint_terrain_value) > 0:
                    mobile_largest_contentful_paint_terrain_value = mobile_largest_contentful_paint_terrain_value[0]
                if mobile_largest_contentful_paint_terrain_value:
                    mobile_largest_contentful_paint_terrain_value = float(mobile_largest_contentful_paint_terrain_value)
                else:
                   mobile_largest_contentful_paint_terrain_value= None 


                  # Mobile_speed_index_lab
                if isinstance(mobile_speed_index_lab_value, tuple) and len(mobile_speed_index_lab_value) > 0:
                   mobile_speed_index_lab_value = mobile_speed_index_lab_value[0]
                if mobile_speed_index_lab_value:
                   mobile_speed_index_lab_value = float(mobile_speed_index_lab_value)
                else:
                   mobile_speed_index_lab_value= None  

                # Mobile_time_to_interactive_lab
                if isinstance(mobile_time_to_interactive_lab_value, tuple) and len(mobile_time_to_interactive_lab_value) > 0:
                   mobile_time_to_interactive_lab_value = mobile_time_to_interactive_lab_value[0]
                if mobile_time_to_interactive_lab_value:
                   mobile_time_to_interactive_lab_value = float(mobile_time_to_interactive_lab_value)
                else:
                   mobile_time_to_interactive_lab_value= None                 

                # Mobile_total_blocking_time_lab
                if isinstance(mobile_total_blocking_time_lab_value, tuple) and len(mobile_total_blocking_time_lab_value) > 0:
                   mobile_total_blocking_time_lab_value = mobile_total_blocking_time_lab_value[0]
                if mobile_total_blocking_time_lab_value:
                   mobile_total_blocking_time_lab_value = float(mobile_total_blocking_time_lab_value)
                else:
                   mobile_total_blocking_time_lab_value= None 

                # SOSEO_yourtext_guru
                if isinstance(soseo_yourtext_guru_value, tuple) and len(soseo_yourtext_guru_value) > 0:
                   soseo_yourtext_guru_value = soseo_yourtext_guru_value[0]
                if soseo_yourtext_guru_value:
                   soseo_yourtext_guru_value = float(soseo_yourtext_guru_value)
                else:
                   soseo_yourtext_guru_value= None
                
                
                data = Data(
                    Thekeyword=row.get('Keyword', ''),
                    Url=row.get('Url', ''),
                    Top10=row.get('Top10', ''),
                    Position=row.get('Position', ''),
                    Http_code_babbar=row.get('HTTP code BABBAR', ''),
                    Ttfb_babbar=row.get('TTFB (en ms) BABBAR', ''),                   
                    Page_value_babbar=row.get('Page Value BABBAR', ''),
                    Page_trust_babbar=row.get('Page Trust BABBAR', ''),
                    Semantic_value_babbar=row.get('Semantic Value BABBAR', ''),
                    Backlinks_babbar=row.get('Backlinks BABBAR', ''),       
                    Backlinks_host_babbar=row.get('Backlinks host BABBAR', ''),
                    Host_outlinks_babbar=row.get('Host Outlinks BABBAR', ''),
                    Outlinks_babbar=row.get('Outlinks BABBAR', ''),
                    Desktop_first_contentful_paint_terrain=row.get('Desktop First Contentful Paint Terrain', ''),
                    Desktop_first_input_delay_terain=row.get('Desktop First Input Delay Terain', ''),
                    Desktop_largest_contentful_paint_terrain=row.get('Desktop Largest Contentful Paint Terrain', ''),
                    Desktop_cumulative_layout_shift_terrain= row.get('Desktop Cumulative Layout Shift Terrain', ''),
                    Desktop_first_contentful_paint_lab= row.get('Desktop First Contentful Paint Lab', ''),
                    Desktop_speed_index_lab= row.get('Desktop Speed Index Lab', ''),
                    Desktop_largest_contentful_paint_lab = row.get('Desktop Largest Contentful Paint Lab', ''),
                    Desktop_time_to_interactive_lab = row.get('Desktop Time to Interactive Lab', ''),
                    Desktop_cumulative_layout_shift_lab = row.get('Desktop Cumulative Layout Shift Lab', ''),
                    Mobile_first_contentful_paint_terrain = mobile_first_contentful_paint_terrain_value,
                    Mobile_first_input_delay_terain = mobile_first_input_delay_terain_value,
                    Mobile_largest_contentful_paint_terrain = mobile_largest_contentful_paint_terrain_value,
                    Mobile_cumulative_layout_shift_terrain = mobile_cumulative_layout_shift_terrain_value,
                    Mobile_first_contentful_paint_lab = mobile_first_contentful_paint_lab_value,
                    Mobile_speed_index_lab = mobile_speed_index_lab_value,
                    Mobile_largest_contentful_paint_lab = mobile_largest_contentful_paint_lab_value,
                    Mobile_time_to_interactive_lab = mobile_time_to_interactive_lab_value,
                    Mobile_total_blocking_time_lab = mobile_total_blocking_time_lab_value,
                    Mobile_cumulative_layout_shift_lab =  mobile_cumulative_layout_shift_lab_value,
                    SOSEO_yourtext_guru = soseo_yourtext_guru_value,
                    DSEO_yourtext_guru= dseo_yourtext_guru_value,
                    Score_1fr = Score_1fr_value,
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
                    Type_1 = row.get('Type-1', ''),
                    Indexability_y = row.get('Indexability_y', ''),
                    Indexability_Status_y = row.get('Indexability Status_y', ''),
                    Title1_score = row.get('Title 1 score', ''),
                    Meta_Description1_score = row.get('Meta Description 1 score', ''),
                    Meta_Keywords1_score = row.get('Meta Keywords 1 score', ''),
                    H1_1_score = row.get('H1-1 score', ''),
                    H1_2_score = h1_2_score_value,
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
"""
# Delete all objects in the Data and Keyword models
Data.objects.all().delete()
Keyword.objects.all().delete()
"""
print("All data and keywords have been deleted.")
  
data_count = Data.objects.count()
keyword_count = Keyword.objects.count()

print(f"Nombre de données (Data) dans la base de données : {data_count}")
print(f"Nombre de mots-clés (Keyword) dans la base de données : {keyword_count}")

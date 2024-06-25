import os
import time
import pandas as pd
import django
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from django.db.models import Q
from functools import reduce
from django.shortcuts import render, redirect
import operator
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
django.setup()
from SEO_Prediction_App.models import Data, Keyword

data_sets_directory = './DataSets'



def process_column(value):
   
    if isinstance(value, tuple) and len(value) > 0:
        value = value[0]

    if value :
        value = float(value)
    else:
        value = 0.0

    return value


# Importez d'abord les mots-clés
def import_keywords_from_csv(directory_path, keyword_searshed, user_instance):
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv") and keyword_searshed in filename:
            csv_path = os.path.join(directory_path, filename)
            df = pd.read_csv(csv_path)
 
            keyword_name = os.path.splitext(filename)[0]

            keyword, _ = Keyword.objects.get_or_create(keyword=keyword_name, user=user_instance)
            

            # Si le Keyword existait déjà, vous pouvez mettre à jour d'autres attributs si nécessaire


# Importez ensuite les données associées à chaque mot-clé


        
def import_data_from_csv_files(directory_path, keyword_searched):
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv") and keyword_searched in filename:
            csv_path = os.path.join(directory_path, filename)
            df = pd.read_csv(csv_path)
        
            for _, row in df.iterrows():
                # ... (rest of your code)
                 Thekeyword = str(row.get('Keyword', ''))
                 Keyword = keyword_searched
                #print(Thekeyword)
                 data_dict = {
                    'Keyword' : Keyword,
                    'Thekeyword': Thekeyword,
                    'Url': row.get('Url', ''),
                    'Top10': row.get('Top10', ''),
                    'Position': process_column(row.get('Position', '')),
                    'Http_code_babbar': process_column(row.get('HTTP code BABBAR', '')),
                    'Ttfb_babbar': process_column(row.get('TTFB (en ms) BABBAR', '')),
                     'Page_value_babbar': process_column(row.get('Page Value BABBAR', '')),
                    'Page_trust_babbar': process_column(row.get('Page Trust BABBAR', '')),
                    'Semantic_value_babbar': process_column(row.get('Semantic Value BABBAR', '')),
                    'Backlinks_babbar': process_column(row.get('Backlinks BABBAR', '')),
                    'Backlinks_host_babbar': process_column(row.get('Backlinks host BABBAR', '')),
                    'Host_outlinks_babbar': process_column(row.get('Host Outlinks BABBAR', '')),
                    'Outlinks_babbar': process_column(row.get('Outlinks BABBAR', '')),
                    'Desktop_first_contentful_paint_terrain': process_column(row.get('Desktop First Contentful Paint Terrain', '')),
                    'Desktop_first_input_delay_terain': process_column(row.get('Desktop First Input Delay Terain', '')),
                    'Desktop_largest_contentful_paint_terrain': process_column(row.get('Desktop Largest Contentful Paint Terrain', '')),
                    'Desktop_cumulative_layout_shift_terrain': process_column(row.get('Desktop Cumulative Layout Shift Terrain', '')),
                    'Desktop_first_contentful_paint_lab': process_column(row.get('Desktop First Contentful Paint Lab', '')),
                    'Desktop_speed_index_lab': process_column(row.get('Desktop Speed Index Lab', '')),
                    'Desktop_total_blocking_time_lab': process_column(row.get('Desktop Total Blocking Time Lab', '')),
                    'Desktop_largest_contentful_paint_lab' : process_column(row.get('Desktop Largest Contentful Paint Lab', '')),
                    'Desktop_time_to_interactive_lab' : process_column(row.get('Desktop Time to Interactive Lab', '')),
                    'Desktop_cumulative_layout_shift_lab' : process_column(row.get('Desktop Cumulative Layout Shift Lab', '')),
                    'Mobile_first_contentful_paint_terrain' : process_column(row.get('Mobile First Contentful Paint Terrain', '')),
                    'Mobile_first_input_delay_terain' : process_column(row.get('Mobile First Input Delay Terain', '')),
                    'Mobile_largest_contentful_paint_terrain' : process_column(row.get('Mobile Largest Contentful Paint Terrain', '')),
                    'Mobile_cumulative_layout_shift_terrain' : process_column(row.get('Mobile Cumulative Layout Shift Terrain', '')),
                    'Mobile_first_contentful_paint_lab' : process_column(row.get('Mobile First Contentful Paint Lab', '')),
                    'Mobile_speed_index_lab' : process_column(row.get('Mobile Speed Index Lab', '')),
                    'Mobile_largest_contentful_paint_lab' : process_column(row.get('Mobile Largest Contentful Paint Lab', '')),
                    'Mobile_time_to_interactive_lab' : process_column(row.get('Mobile Time to Interactive Lab', '')),
                    'Mobile_total_blocking_time_lab' : process_column(row.get('Mobile Total Blocking Time Lab', '')),
                    'Mobile_cumulative_layout_shift_lab' : process_column(row.get('Mobile Speed Index Lab', '')),
                    'SOSEO_yourtext_guru' : process_column(row.get('SOSEO yourtext_guru', '')),
                    'DSEO_yourtext_guru' : process_column(row.get('DSEO yourtext_guru', '')),
                    'Score_1fr' : process_column(row.get('Score_1fr', '')),
                    'Content_type' : row.get('Content Type', ''),
                    'Status_code' : row.get('Status Code', ''),
                    'Status': row.get('Status', ''),
                    'Indexability_x' : row.get('Indexability_x', ''),
                    'Indexability_status_x' : row.get('Indexability Status_x', ''),
                    'Title1' : row.get('Title 1', ''),
                    'Title1_length' : row.get('Title 1 Length', ''),
                    'Title1_pixel_width' : row.get('Title 1 Pixel Width', ''),
                    'Title2' : row.get('Title 2', ''),
                    'Title2_length' : row.get('Title 2 Length', ''),
                    'Title2_pixel_width' : row.get('Title 2 Pixel Width', ''),
                    'Meta_description1' : row.get('Meta Description 1', ''),
                    'Meta_description1_length' : row.get('Meta Description 1 Length', ''),
                    'Meta_description1_Pixel_width': row.get('Meta Description 1 Pixel Width', ''),
                    'Meta_description2' : row.get('Meta Description 2', ''), 
                    'Meta_description2_length' : process_column(row.get('Meta Description 2 Length', '')),
                    'Meta_description2_Pixel_width' : process_column(row.get('Meta Description 2 Pixel Width', '')),
                    'Meta_Keywords1' : row.get('Meta Keywords 1', ''),
                    'Meta_keywords1_length' : row.get('Meta Keywords 1 Length', ''),
                    'H1_1' : row.get('H1-1', ''),
                    'H1_1_length' : row.get('H1-1 Length', ''),
                    'H1_2' : row.get('H1-2', ''),
                    'H1_2_length' : row.get('H1-2 Length', ''),
                    'H2_1' : row.get('H2-1', ''),
                    'H2_1_length' : row.get('H2-1 Length', ''),
                    'H2_2' : row.get('H2-2', ''),
                    'H2_2_length' : row.get('H2-2 Length', ''),
                    'Meta_robots_1' : row.get('Meta Robots 1', ''),
                    'Meta_robots_2' : row.get('Meta Robots 2', ''),
                    'Meta_robots_3' : row.get('Meta Robots 3', ''),
                    'X_robots_tag1' : row.get('X-Robots-Tag 1', ''),
                    'Meta_Refresh_1' : row.get('Meta Refresh 1', ''),
                    'Canonical_link_element1' : row.get('Canonical Link Element 1', ''),
                    'Canonical_link_element2' : row.get('Canonical Link Element 2', ''),
                    'rel_next_1' : row.get('rel="next" 1', ''),
                    'rel_prev_1' : row.get('rel="prev" 1', ''),
                    'HTTP_rel_next_1' : row.get('HTTP rel="next" 1', ''),
                    'HTTP_rel_prev_1' : row.get('HTTP rel="prev" 1', ''),
                    'amphtml_link_element' : row.get('amphtml Link Element', ''),
                    'Size_bytes' : process_column(row.get('Size (bytes)', '')),
                    'Word_count' : process_column(row.get('Word Count', '')),
                    'Sentence_Count' : process_column(row.get('Sentence Count', '')),
                    'Average_words_per_sentence' : row.get('Average Words Per Sentence', ''),
                    'Flesch_reading_ease_score' : process_column(row.get('Flesch Reading Ease Score', '')),
                    'Readability' : row.get('Readabilit', ''),
                    'Text_ratio' : row.get('Text Ratio', ''),
                    'Crawl_depth' : process_column(row.get('Crawl Depth', '')),
                    'Link_score' : process_column(row.get('Link Score', '')),
                    'Inlinks' : process_column(row.get('Inlinks', '')),
                    'Unique_inlinks' : process_column(row.get('Unique Inlinks', '')),
                    'Unique_JS_inlinks' : row.get('Unique JS Inlinks', ''),
                    'of_Total' : process_column(row.get('% of Total', '')),
                    'Outlinks' : process_column(row.get('Outlinks', '')),
                    'Unique_Outlinks' : process_column(row.get('Unique Outlinks', '')),
                    'Unique_JS_Outlinks' : row.get('Unique JS Outlinks', ''),
                    'External_Outlinks' : process_column(row.get('External Outlinks', '')),
                    'Unique_External_Outlinks' : process_column(row.get('Unique External Outlinks', '')),
                    'Unique_External_JS_Outlinks' : process_column(row.get('Unique External JS Outlinks', '')),
                    'Closest_Similarity_Match' : process_column(row.get('Closest Similarity Match', '')),
                    'NoNear_Duplicates' : process_column(row.get('No. Near Duplicates', '')),
                    'Spelling_Errors' : process_column(row.get('Spelling Errors', '')),
                    'Grammar_Errors' : process_column(row.get('Grammar Errors', '')),
                    'Hash' : row.get('Hash', ''),
                    'Response_time' : row.get('Response Time', ''),
                    'Last_modified' : row.get('Last Modified', ''),
                    'Redirect_URL' : row.get('Redirect URL', ''),
                    'Redirect_type' : row.get('Redirect Type', ''),
                    'Cookies' : row.get('Cookies', ''),
                    'HTTP_Version' : process_column(row.get('HTTP Version', '')),
                    'URL_Encoded_Address' : row.get('URL Encoded Address', ''),
                    'Crawl_Timestamp' : row.get('Crawl Timestamp', ''),
                    'Errors' : row.get('Errors', ''),
                    'Warnings' : process_column(row.get('Warnings', '')),
                    'Total_Types' : process_column(row.get('Total Types', '')),
                    'Unique_Types' : row.get('Unique Types', ''),
                    'Type_1' : process_column(row.get('Type 1', '')),
                    'Indexability_y' : row.get('Indexability_y', ''),
                    'Indexability_Status_y' : row.get('Indexability Status_y', ''),
                    'Title1_score' : process_column(row.get('Title 1 score', '')),
                    'Meta_Description1_score' : process_column(row.get('Meta Description 1 score', '')),
                    'Meta_Keywords1_score' : process_column(row.get('Meta Keywords 1 score', '')),
                    'H1_1_score' : process_column(row.get('H1-1 score', '')),
                    'H1_2_score' : process_column(row.get('H1-2 score', '')),
                    'H2_1_score' : process_column(row.get('H2-1 score', '')),
                    'H2_2_score' : process_column(row.get('H2-2 score', '')),
                    'Meta_Robots_1_score' : process_column(row.get('Meta Robots 1 score', '')),
                    'Url_Score' : process_column(row.get('Url score', '')),
                }
                
                 #unique_key_columns = ['Thekeyword']
                 #unique_key_values = {column: data_dict[column] for column in unique_key_columns}
                 unique_key_columns = list(data_dict.keys())
                 unique_key_values = {column: data_dict[column] for column in unique_key_columns}
                 print("****j'affiche****",unique_key_values)
                 print("*******the data from database****", Data.objects)
                 existing_entry = Data.objects.filter(**unique_key_values).first()

                 if not existing_entry:
                    data = Data(**data_dict)
                    data.save()
                 else:
                    # Si une correspondance est trouvée, affichez un message
                    print(f"Doublon trouvé, enregistrement non ajouté : {data_dict}")
                                 # Vérifiez si une entrée similaire existe déjà dans la base de données
            print(data_dict)
    remove_duplicates_in_database()

def delete_csv_file(directory_path, keyword_searched):
    for filename in os.listdir(directory_path):
       # Vérifier si le fichier se termine par ".csv" et contient le mot-clé recherché
        if filename.endswith(".csv") and keyword_searched in filename:
            # Construire le chemin complet vers le fichier
            csv_path = os.path.join(directory_path, filename)
            # Supprimer le fichier
            os.remove(csv_path)
            print(f"File {filename} deleted")



def remove_duplicates_in_database():
    # Ajoutez toutes les colonnes nécessaires pour construire la clé unique
    unique_key_columns = [
        'Thekeyword','Keyword', 'Position', 'Url', 'Top10', 'Http_code_babbar', 'Ttfb_babbar',
        'Page_value_babbar', 'Page_trust_babbar', 'Semantic_value_babbar', 'Backlinks_babbar',
        'Backlinks_host_babbar', 'Host_outlinks_babbar', 'Outlinks_babbar', 'Desktop_first_contentful_paint_terrain', 
        'Desktop_first_input_delay_terain', 'Desktop_largest_contentful_paint_terrain', 'Desktop_cumulative_layout_shift_terrain',
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
        'Meta_Keywords1_score', 'Meta_Keywords1_score', 'H1_1_score', 'H1_2_score', 'H2_1_score', 'H2_2_score', 'Meta_Robots_1_score', 'Url_Score'  
    ]

     # Identifiez les doublons en utilisant la méthode distinct de Django
    duplicates_to_remove = Data.objects.values(*unique_key_columns).annotate(count=Count('id')).filter(count__gt=1)
   
    for duplicate in duplicates_to_remove:
        duplicate_key_values = ', '.join(f"{key}: {duplicate[key]}" for key in unique_key_columns)
        print(f"Pour les valeurs {duplicate_key_values}, le nombre de doublons est {duplicate['count']}.")

    # Supprimez les doublons
    for duplicate in duplicates_to_remove:
        # Excluez l'instance que vous souhaitez conserver (par exemple, avec l'id minimum)
        instance_to_keep = Data.objects.filter(**{column: duplicate[column] for column in unique_key_columns}).order_by('id').first()
        
        # Excluez toutes les autres instances
        instances_to_delete = Data.objects.filter(**{column: duplicate[column] for column in unique_key_columns}).exclude(id=instance_to_keep.id)
        
        # Supprimez les instances
        instances_to_delete.delete()


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".csv"):
            print(f"Modification détectée dans le fichier: {event.src_path}")
            try:
                import_keywords_from_csv(data_sets_directory, "voyage")
                import_data_from_csv_files(data_sets_directory, "voyage")
            except pd.errors.EmptyDataError:
                print(f"Le fichier {event.src_path} est vide ou ne contient pas de colonnes.")
            except Exception as e:
                print(f"Erreur lors de la mise à jour des données : {e}")


def my_view(request):
    if request.user.is_authenticated:
        print("testtetstetstetstet")
        user_name = request.user.username
        context = {
            'user_name': user_name
        }
        print(user_name)
        return render(request, '/header.html', context)    

"""if __name__ == "__main__":
   
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
Data.objects.all().delete()
Keyword.objects.all().delete()

print("All data and keywords have been deleted.")
  
data_count = Data.objects.count()
keyword_count = Keyword.objects.count()

print(f"Nombre de données (Data) dans la base de données : {data_count}")
print(f"Nombre de mots-clés (Keyword) dans la base de données : {keyword_count}")

#remove_duplicates_in_database()    
"""
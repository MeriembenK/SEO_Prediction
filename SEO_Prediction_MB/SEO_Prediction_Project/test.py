import os
import django
from import_data_url import import_data_url_from_csv_files

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
django.setup() 
from Predictive.data_colector import DataColector 
from Predictive.url_Predict import UrlPredect
from import_data import import_data_from_csv_files, import_keywords_from_csv,remove_duplicates_in_database


dc = DataColector()


# Appelez la méthode get_keywords
keyword_searched = "Hôtel"  # Remplacez par votre propre mot-clé
similar_keywords = dc.get_keywords(keyword_searched)
print("Mots-clés similaires pour", keyword_searched, ":")
print(similar_keywords)

# Appelez la méthode get_Data_as_csv2 pour traiter les données
"""nb_sim_keywords = 20
nb_links = 100
nb_top_1 = 10
"""
nb_sim_keywords = 3
nb_links = 10
nb_top_1 = 10


res_df = dc.get_Data_as_csv2(keyword_searched, nb_sim_keywords, nb_links, nb_top_1)
print("Données traitées pour le mot-clé", keyword_searched, ":")
print(res_df)

data_sets_directory = './DataSets'

import_keywords_from_csv(data_sets_directory, keyword_searched)
import_data_from_csv_files(data_sets_directory, keyword_searched)
remove_duplicates_in_database()

"""url_predictor = UrlPredect() 
data_sets = "./Url_data"
import_data_url_from_csv_files(data_sets)

df_url= url_predictor.get_data_url_from_database()

print(df_url)"""
"""start_url= "https://www.agence-naga.fr/expertise/webmarketing/referencement-naturel-seo-lyon/"
keyword= "agence seo nantes referencement44fr"
res_df = dc.get_Data_as_csv3(start_url, keyword)
print("Données traitées pour l'url", ":")
"""




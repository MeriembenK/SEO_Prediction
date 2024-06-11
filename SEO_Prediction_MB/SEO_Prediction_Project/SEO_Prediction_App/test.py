import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
django.setup() 
from Predictive.data_colector import DataColector 
from Predictive.url_Predict import UrlPredect
from .import_data import import_data_from_csv_files, import_keywords_from_csv
from SEO_Prediction_App.models import Data, Keyword
from django.http import HttpRequest 
from django.contrib.auth.models import User
from django.test import RequestFactory

def run_script_with_keyword(keyword_searched, user_instance):
    dc = DataColector()

    # Appelez la méthode get_keywords
    similar_keywords = dc.get_keywords(keyword_searched)
    print("Mots-clés similaires pour", keyword_searched, ":")
    print(similar_keywords)

    # Appelez la méthode get_Data_as_csv2 pour traiter les données
    nb_sim_keywords = 4
    nb_links = 20
    nb_top_1 = 10

    Data.objects.filter(Keyword=keyword_searched).delete()
    Keyword.objects.filter(keyword=keyword_searched).delete()

    res_df = dc.get_Data_as_csv2(keyword_searched, nb_sim_keywords, nb_links, nb_top_1)
    print("Données traitées pour le mot-clé", keyword_searched, ":")
    print(res_df)

    data_sets_directory = './DataSets'
    print(f"user_instance in run_script_with_keyword: {type(user_instance)}")
    print("on affiche le user_instance", user_instance)
    
    import_keywords_from_csv(data_sets_directory, keyword_searched, user_instance)
    import_data_from_csv_files(data_sets_directory, keyword_searched)


"""tests = Test.objects.all()

# Supprimer chaque enregistrement un par un
for test in tests:
    test.delete()"""

"""dc = DataColector()


# Appelez la méthode get_keywords
keyword_searched = "Hôtel"  # Remplacez par votre propre mot-clé
similar_keywords = dc.get_keywords(keyword_searched)
print("Mots-clés similaires pour", keyword_searched, ":")
print(similar_keywords)

# Appelez la méthode get_Data_as_csv2 pour traiter les données
nb_sim_keywords = 20
nb_links = 100
nb_top_1 = 10

nb_sim_keywords = 3
nb_links = 20
nb_top_1 = 10

Data.objects.filter(Keyword=keyword_searched).delete()
Keyword.objects.filter(Keyword=keyword_searched).delete()

res_df = dc.get_Data_as_csv2(keyword_searched, nb_sim_keywords, nb_links, nb_top_1)
print("Données traitées pour le mot-clé", keyword_searched, ":")
print(res_df)

data_sets_directory = './DataSets'

import_keywords_from_csv(data_sets_directory, keyword_searched)
import_data_from_csv_files(data_sets_directory, keyword_searched)
"""
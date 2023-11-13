import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
django.setup() 

from Predictive.data_colector import DataColector 
import pandas as pd
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from fake_useragent import UserAgent
import random

dc = DataColector()

# Appelez la méthode get_keywords
keyword = "voyage"  # Remplacez par votre propre mot-clé
similar_keywords = dc.get_keywords(keyword)
print("Mots-clés similaires pour", keyword, ":")
print(similar_keywords)

# Appelez la méthode get_Data_as_csv2 pour traiter les données
nb_sim_keywords = 3
nb_links = 2
nb_top_1 = 2
res_df = dc.get_Data_as_csv2(keyword, nb_sim_keywords, nb_links, nb_top_1)  # Remplacez les valeurs par les vôtres
print("Données traitées pour le mot-clé", keyword, ":")
print(res_df)



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
#from Predictive.train_Models import TrainModels

dc = DataColector()

# Appelez la méthode get_keywords
keyword = "Fiat"  # Remplacez par votre propre mot-clé
similar_keywords = dc.get_keywords(keyword)
print("Mots-clés similaires pour", keyword, ":")
print(similar_keywords)

# Appelez la méthode get_Data_as_csv2 pour traiter les données
nb_sim_keywords = 3
nb_links = 2
nb_top_1 = 2
res_df = dc.get_Data_as_csv2(keyword, nb_sim_keywords, nb_links, nb_top_1)
print("Données traitées pour le mot-clé", keyword, ":")
print(res_df)


"""
# Create an instance of TrainModels
trainer = TrainModels()

# Call the read_my_data method
trainer.read_my_data()

# Access the DataFrames created by the method
data_df = trainer.df


# Print the first few rows of each DataFrame to check the data
print("Data DataFrame:")
print(data_df.head())

data_df = trainer.data_to_drop(data_df)

# Print the cleaned DataFrame
print("Cleaned DataFrame:")
print(data_df)

print("Columns in the DataFrame:")
print(data_df.columns)
"""



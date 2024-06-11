import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
django.setup() 
from Predictive.train_Models import TrainModels
from Predictive.url_Predict import UrlPredect
from Predictive.response_Builder import ResponseBuilder
from Predictive.url_Predict import UrlPredect
from import_data_url import import_data_url_from_csv_files
import pandas as pd
import re


#initialisatioon de response_builder et train_models
response_builder = ResponseBuilder()
trainer = TrainModels()
up = UrlPredect()

#specific_url = "https://fr.igraal.com/avis/Go-Voyages"
specific_url = "https://www.sortlist.fr/seo/paris-fr" 
keyword = "voyage"


# Lexture de la data depuis la bdd
trainer.keyword = keyword
df= trainer.read_my_data_for_url()
trainer.df= df
print(trainer.df)

trainer.df = trainer.df.drop(columns=["Keyword"])
trainer.df = trainer.df.drop(columns=["Url"])
trainer.df = trainer.data_to_drop(trainer.df)
trainer.preprocessing()
print(trainer.df)

response_builder.df = trainer.df
print(response_builder.df)


X_train, X_test, y_train, y_test = trainer.split_data(trainer.X, trainer.y)

trained_model= trainer.train_XGBClassifier(X_train, y_train)
auc, acc = trainer.eval_model(trained_model,X_test, y_test)
print(auc, acc)
df_importance = trainer.get_importance(trained_model)
df_importance_top_15 = df_importance.head(15)
print("Les 15 fonctionnalités les plus importantes :")
print(df_importance_top_15)

trained_model.y = y_train
response_builder.trainedModels= trained_model


data_test, testing = up.get_data_for_1_urls(specific_url,keyword,df, response_builder)

print("data test & testing", data_test, testing)



if testing == False :
  csv_filename = './Url_data/url_data_output.csv'
  up.url_data.to_csv(csv_filename, index=False)
  print(f"Data saved to {csv_filename}")

  data_sets = "./Url_data"
  import_data_url_from_csv_files(data_sets)


thedf_test= up.get_data_url_from_database()
print(thedf_test)

up.url_data = thedf_test

up.url_data=up.exclude_and_convert_columns(up.url_data)

result, pred_res = up.try_for_columns(trained_model, response_builder)
print(pred_res)


df_min_max = response_builder.get_min_max_url()
print(df_min_max)

# Filtrer les résultats pour ne conserver que les 15 premières fonctionnalités importantes
top_15_columns = df_importance_top_15['variable'].tolist()
df_min_max_top_15 = df_min_max[top_15_columns]

print("Les résultats min-max pour les 15 premières fonctionnalités importantes :")
print(df_min_max_top_15)













































"""data_test = url_predictor.url_data
data_test=url_predictor.exclude_and_convert_columns(data_test)

# Assurez-vous que ma donnée test a les mêmes colonnes que trained_model.feature_names_
data_test = data_test[X_train.columns].reset_index(drop=True)
print("Colonnes de la donnée de test en dehors de la fonction try_for_columns:", data_test.columns)
url_predictor.url_data = data_test    

# Appeler la fonction try_for_columns avec le modèle entraîné pour prédir pour la donnée test 
result = url_predictor.try_for_columns(trained_models, response_builder)
print(result)"""

"""X_train, X_test, y_train, y_test = trainer.split_data(trainer.X, trainer.y)
trained_model= trainer.train_XGBClassifier(X_train, y_train)
auc, acc = trainer.eval_model(trained_model,X_test, y_test)
print(auc, acc)

"""
    

"""df = url_predictor.get_data_from_database(keyword)
print(df)

trainer = TrainModels()
trainer.df = df
print("THE DF", trainer.df)

trainer.train_model(trainer.df)"""

"""if not df.empty:
    num_columns = df.shape[1]
    print("Nombre de colonnes dans data_dr :", num_columns)

    url_predictor.url = specific_url
    url_predictor.keyword = keyword

    print("the url", url_predictor.url)
    print("the key word", keyword)

    # Obtenir des données pour l'URL et le mot-clé spécifiés
    url_predictor.url_data, testing = url_predictor.get_data_for_url_keyword(specific_url, keyword, df, response_builder)
    print("la valeur de testing est égale à ", testing)
    print("The url_data is", url_predictor.url_data)

    if testing==True:
       print("Message : df_key_url.head existe.")
       print("The url_data is", url_predictor.url_data)
   
   
    else:
       
       print("Message : df_key_url.head n'existe pas.")
       print("The url_data is", url_predictor.url_data)
       
        #print("data url ::",url_predictor.url_data)
       csv_filename = './Url_data/url_data_output.csv'
       url_predictor.url_data.to_csv(csv_filename, index=False)
       print(f"Data saved to {csv_filename}")

       data_sets = "./Url_data"
       import_data_url_from_csv_files(data_sets)

       df_url= url_predictor.get_data_url_from_database()
       url_predictor.url_data, testing = url_predictor.get_data_for_url(specific_url, keyword, df_url, response_builder)
       print("Columns, types, and values in url_predictor.url_data:")
       for index, row in url_predictor.url_data.iterrows():
            print(f"\nRow {index + 1}:")
            for column in url_predictor.url_data.columns:
               column_type = url_predictor.url_data[column].dtype
               column_value = row[column]
               print(f"  {column} ({column_type}): {column_value}")
       print("je vais afficher pour regarder .................................................")
       print("The url_data is", url_predictor.url_data)
    
else:
    print("Le DataFrame est vide. Veuillez vérifier les données chargées.")"""


"""
all_site_urls = dc.get_all_site_urls(start_url, 3)
print(all_site_urls)
print("Nombre de liens :", len(all_site_urls))


# Accéder aux DataFrames créés par la méthode
trainer.df = trainer.data_to_drop(trainer.df)
# Prétraitement de la data
trainer.preprocessing()

#Split data entre data d'entrainement et la data du test
X_train, X_test, y_train, y_test = trainer.split_data(trainer.X, trainer.y)

columns_with_nan = trainer.df.columns[trainer.df.isnull().any()].tolist()

# Afficher les colonnes avec des valeurs NaN, leur nombre de valeurs NaN respectif et leur type
nan_info = pd.DataFrame({
    'Colonnes': columns_with_nan,
    'Nombre de NaN': trainer.df[columns_with_nan].isnull().sum().tolist(),
    'Type': trainer.df[columns_with_nan].dtypes.tolist()
})

print("Informations sur les colonnes avec des valeurs NaN :\n", nan_info)



url_predictor = UrlPredect()


df = url_predictor.get_data_from_database()

if not df.empty:
    num_columns = df.shape[1]
    print("Nombre de colonnes dans data_dr :", num_columns)

    specific_url = 'https://www.promovacances.com/billet-avion/vol-maroc/pays,149/'
    keyword = 'Billet d\'avion maroc'


    url_predictor.url = specific_url
    url_predictor.keyword = keyword

    print("the url", url_predictor.url)
    print("the key word", keyword)

    # Obtenir des données pour l'URL et le mot-clé spécifiés
    url_predictor.url_data, testing = url_predictor.get_data_for_url_keyword(specific_url, keyword, df, response_builder)
    print("la valeur de testing est égale à ", testing)
    print("The url_data is", url_predictor.url_data)

    if testing==True:
       print("Message : df_key_url.head existe.")
       print("The url_data is", url_predictor.url_data)
   
   
    else:
       
       print("Message : df_key_url.head n'existe pas.")
       print("The url_data is", url_predictor.url_data)
       
        #print("data url ::",url_predictor.url_data)
       csv_filename = './Url_data/url_data_output.csv'
       url_predictor.url_data.to_csv(csv_filename, index=False)
       print(f"Data saved to {csv_filename}")

       data_sets = "./Url_data"
       import_data_url_from_csv_files(data_sets)

       df_url= url_predictor.get_data_url_from_database()
       url_predictor.url_data, testing = url_predictor.get_data_for_url(specific_url, keyword, df_url, response_builder)
       print("Columns, types, and values in url_predictor.url_data:")
       for index, row in url_predictor.url_data.iterrows():
            print(f"\nRow {index + 1}:")
            for column in url_predictor.url_data.columns:
               column_type = url_predictor.url_data[column].dtype
               column_value = row[column]
               print(f"  {column} ({column_type}): {column_value}")
       print("je vais afficher pour regarder .................................................")
       print("The url_data is", url_predictor.url_data)
    
else:
    print("Le DataFrame est vide. Veuillez vérifier les données chargées.")


# Exclure et convertir les colonnes 
colonnes_exclues = ['Thekeyword','Url']
df = df.drop(columns=colonnes_exclues, errors='ignore')
trainer.df = df
num_columns = trainer.df.shape[1]
print("Nombre de colonnes dans data_dr :", num_columns)

#Prétraitement de la data test
data= url_predictor.exclude_and_convert_columns(trainer.df)
num_columns = data.shape[1]
print("Nombre de colonnes dans data_dr :", num_columns)
trainer.df = data
int_columns = trainer.df.select_dtypes(include='int').columns
print("int columns:", int_columns)

#Entrainement de données
trainer.preprocessing()
X_train, X_test, y_train, y_test = trainer.split_data(trainer.X, trainer.y)
trained_model= trainer.train_XGBClassifier(X_train, y_train)
auc, acc = trainer.eval_model(trained_model,X_test, y_test)
print(auc, acc)



response_builder.trainedModels= trained_model
response_builder.df = trainer.df 
response_builder.trainedModels.y = y_train
data_test = url_predictor.url_data
data_test=url_predictor.exclude_and_convert_columns(data_test)

# Assurez-vous que ma donnée test a les mêmes colonnes que trained_model.feature_names_
data_test = data_test[X_train.columns].reset_index(drop=True)
print("Colonnes de la donnée de test en dehors de la fonction try_for_columns:", data_test.columns)
url_predictor.url_data = data_test    

# Appeler la fonction try_for_columns avec le modèle entraîné pour prédir pour la donnée test 
result = url_predictor.try_for_columns(trained_model, response_builder)
print(result)

"""


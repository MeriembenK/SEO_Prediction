import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
django.setup() 

from Predictive.train_Models import TrainModels
from import_data_url import import_data_url_from_csv_files
from Predictive.url_Predict import UrlPredect
from Predictive.response_Builder import ResponseBuilder
import pandas as pd


# Initialisation de la classe TrainModels
trainer = TrainModels()

# Read data from Data Base
trainer.read_my_data()

# Accéder aux DataFrames créés par la méthode
data_df = trainer.df

# Suppression des colonnes inutiles
data_df = trainer.data_to_drop(data_df)
trainer.df = data_df

# Prétraitement de la data
trainer.preprocessing()

# Afficher chaque colonne avec son type

#Split data entre data d'entrainement et la data du test
X_train, X_test, y_train, y_test = trainer.split_data(trainer.X, trainer.y)



"*************************Testing models**********************************"

#test des modèles de bases
model , auc , acc , importance_score= trainer.train_model(trainer.train_RandomForestClassifier)
print("The AUC",auc)
print("The ACC",acc)
print("The importance scores", importance_score)

#trained_model = trainer.train_models(trainer.df)
#Test modèle ensembliste
#trainer.Final_get_importance()



































#Initialisation des classes TrainModels, UrlPredect, ResponseBuilder
trainer = TrainModels()
url_predictor = UrlPredect()
response_builder = ResponseBuilder()



#Charger les données de la base de données
df = url_predictor.get_data_from_database()

if not df.empty:
    num_columns = df.shape[1]
    print("Nombre de colonnes dans data_dr :", num_columns)

    # Définir l'URL spécifique et le mot-clé
    specific_url = 'https://www.govoyages.com/compagnie-aerienne/2C/sncf/'
    keyword = 'voyages sncf'
    url_predictor.url = specific_url
    url_predictor.keyword = keyword

    print("the url", url_predictor.url)
    print("the key word", keyword)

    # Obtenir des données pour l'URL et le mot-clé spécifiés
    url_predictor.url_data = url_predictor.get_data_for_url(specific_url, keyword, df, response_builder)
    if isinstance(url_predictor.url_data, pd.DataFrame) and not url_predictor.url_data.empty:
       print("Message : df_key_url.head existe.")
       print()
    else:
       print("Message : df_key_url.head n'existe pas.")
    #print("data url ::",url_predictor.url_data)
       csv_filename = './Url_data/url_data_output.csv'
       url_predictor.url_data.to_csv(csv_filename, index=False)
       print(f"Data saved to {csv_filename}")

       data_sets = "./Url_data"
       import_data_url_from_csv_files(data_sets)
    
else:
    print("Le DataFrame est vide. Veuillez vérifier les données chargées.")
print("this is : ******URL_data*******",url_predictor.url_data)

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
"""
"""
#Entrainement de données
trainer.preprocessing()
X_train, X_test, y_train, y_test = trainer.split_data(trainer.X, trainer.y)
trained_model= trainer.train_RandomForestClassifier(X_train, y_train)
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

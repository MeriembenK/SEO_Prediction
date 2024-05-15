import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
django.setup() 

from Predictive.train_Models import TrainModels
from import_data_url import import_data_url_from_csv_files
from Predictive.url_Predict import UrlPredect
from Predictive.response_Builder import ResponseBuilder
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Predictive.data_colector import DataColector 
from SEO_Prediction_App.models import Keyword
<<<<<<< HEAD
from SEO_Prediction_App import test
=======
>>>>>>> 380f5623e5454e10dcc670b83a03d4ff2b7896ab

# Récupérer tous les mots-clés depuis la base de données
keywords = Keyword.objects.all()

<<<<<<< HEAD
=======
# Récupérer tous les mots-clés depuis la base de données
keywords = Keyword.objects.all()

>>>>>>> 380f5623e5454e10dcc670b83a03d4ff2b7896ab
# Afficher les options disponibles à l'utilisateur
print("Choisissez le mot-clé :")
for index, keyword in enumerate(keywords, start=1):
    print(f"{index}. {keyword.Keyword}")
<<<<<<< HEAD

# Demander à l'utilisateur de saisir le numéro du mot-clé
selected_keyword_index = int(input("Entrez le numéro du mot-clé que vous souhaitez : "))

# Vérifier si le numéro saisi est valide
if 1 <= selected_keyword_index <= len(keywords):
    # Récupérer le mot-clé sélectionné par l'utilisateur
    selected_keyword = keywords[selected_keyword_index - 1]
    print(f"Vous avez choisi le mot-clé : {selected_keyword.Keyword}")
else:
    print("Numéro de mot-clé invalide.")
=======

# Demander à l'utilisateur de saisir le numéro du mot-clé
selected_keyword_index = int(input("Entrez le numéro du mot-clé que vous souhaitez : "))

# Vérifier si le numéro saisi est valide
if 1 <= selected_keyword_index <= len(keywords):
    # Récupérer le mot-clé sélectionné par l'utilisateur
    selected_keyword = keywords[selected_keyword_index - 1]
    print(f"Vous avez choisi le mot-clé : {selected_keyword.Keyword}")
else:
    print("Numéro de mot-clé invalide.")

# Initialisation de la classe TrainModels
trainer = TrainModels()
response_builder = ResponseBuilder()
trainer.keyword= selected_keyword.Keyword

# Read data from Data Base
trainer.read_my_data()
nombre_lignes = trainer.df.shape[0]
print("Nombre de lignes dans le DataFrame:", nombre_lignes)

# Accéder aux DataFrames créés par la méthode
trainer.df = trainer.data_to_drop(trainer.df)
response_builder.df= trainer.df

# Prétraitement de la data
trainer.preprocessing()
>>>>>>> 380f5623e5454e10dcc670b83a03d4ff2b7896ab

#Split data entre data d'entrainement et la data du test
X_train, X_test, y_train, y_test = trainer.split_data(trainer.X, trainer.y)

<<<<<<< HEAD
test.run_script_with_keyword(selected_keyword)

# Initialisation de la classe TrainModels
trainer = TrainModels()
=======
# Display the number of elements in each set
print("Number of elements in X_train:", X_train.shape[0])
print("Number of elements in y_train:", y_train.shape[0])
print("Number of elements in X_test:", X_test.shape[0])
print("Number of elements in y_test:", y_test.shape[0])

"*************************Testing models**********************************"
"""stack_model, X_test_stack, y_test_stack, Model1, Model2, Model3, Model4, Model5= trainer.train_and_evaluate_stacking(X_train, y_train, X_test, y_test, n_folds=5)
auc, acc= trainer.eval_model(stack_model, X_test_stack, y_test_stack)
print(auc)
print("The accuracy",acc)"""

trainer.Final_get_importance()

fig, percentage_top, percentage_not_top = response_builder.get_percentage_of_classes()
print("Pourcentage des non Top",percentage_not_top)
print("Pourcentage des Top",percentage_top)

"""*********************************************************Testing récupération url site****************************************************************************"""

"""url_predictor = UrlPredect()
df = url_predictor.get_data_from_database()
dc = DataColector()"""

"""
# Utilisez la méthode get_all_site_urls à partir de l'instance
start_url = "https://www.agence-naga.fr/expertise/webmarketing/referencement-naturel-seo-lyon/"
keyword = "agence seo nantes referencement44fr"
>>>>>>> 380f5623e5454e10dcc670b83a03d4ff2b7896ab
response_builder = ResponseBuilder()
trainer.keyword = selected_keyword
print("****************************Trainer.keyword is ***********************", trainer.keyword)

<<<<<<< HEAD
=======


all_site_urls = dc.get_all_site_urls(start_url, 3)
print(all_site_urls)
print("Nombre de liens :", len(all_site_urls))


trainer = TrainModels()
>>>>>>> 380f5623e5454e10dcc670b83a03d4ff2b7896ab
# Read data from Data Base
trainer.read_my_data()
trainer.df = trainer.data_to_drop(trainer.df)
trainer.preprocessing()
<<<<<<< HEAD
trainer.Final_get_importance()



"""if not df.empty:
    num_columns = df.shape[1]
    print("Nombre de colonnes dans data_dr :", num_columns)

    specific_url = 'https://www.promovacances.com/billet-avion/vol-maroc/pays,149/'
    keyword = 'Billet d\'avion maroc'
=======

#Split data entre data d'entrainement et la data du test
X_train, X_test, y_train, y_test = trainer.split_data(trainer.X, trainer.y)

columns_with_nan = trainer.df.columns[trainer.df.isnull().any()].tolist()

# Afficher les colonnes avec des valeurs NaN, leur nombre de valeurs NaN respectif et leur type
nan_info = pd.DataFrame({
    'Colonnes': columns_with_nan,
    'Nombre de NaN': trainer.df[columns_with_nan].isnull().sum().tolist(),
    'Type': trainer.df[columns_with_nan].dtypes.tolist()
})

print("Informations sur les colonnes avec des valeurs NaN :\n", nan_info)"""



"""url_predictor = UrlPredect()


df = url_predictor.get_data_from_database()

if not df.empty:
    num_columns = df.shape[1]
    print("Nombre de colonnes dans data_dr :", num_columns)

    specific_url = 'https://www.premiereclasse.com/fr-fr/'
    keyword = 'hôtel première classe'
>>>>>>> 380f5623e5454e10dcc670b83a03d4ff2b7896ab


    url_predictor.url = specific_url
    url_predictor.keyword = keyword

    print("the url", url_predictor.url)
    print("the key word", keyword)

    # Obtenir des données pour l'URL et le mot-clé spécifiés
    url_predictor.url_data, testing = url_predictor.get_data_for_url_keyword(specific_url, keyword, df, responseBuilder)
    print("la valeur de testing est égale à ", testing)
    print("The url_data is", url_predictor.url_data)

    if testing==True:
       print("Message : df_key_url.head existe.")
       print("Colonnes avec leurs types de données:")
       for i, (col, dtype) in enumerate(url_predictor.url_data.dtypes.items()):
            print(f"{i}: {col} (type: {dtype})")
   
   
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
       url_predictor.url_data, testing = url_predictor.get_data_for_url(specific_url, keyword, df_url, responseBuilder)
       print("Columns, types, and values in url_predictor.url_data:")
       for index, row in url_predictor.url_data.iterrows():
            print(f"\nRow {index + 1}:")
            for column in url_predictor.url_data.columns:
               column_type = url_predictor.url_data[column].dtype
               column_value = row[column]
               print(f"  {column} ({column_type}): {column_value}")
       print("je vais afficher pour regarder .................................................")
       print("Colonnes avec leurs types de données:")
       for i, (col, dtype) in enumerate(url_predictor.url_data.dtypes.items()):
          print(f"{i}: {col} (type: {dtype})")
    
else:
    print("Le DataFrame est vide. Veuillez vérifier les données chargées.")"""

















"""


specific_url = 'https://www.promovacances.com/billet-avion/vol-maroc/pays,149/'
keyword = 'Billet d\'avion maroc'

print("Printing the specific url : ",specific_url)
print("printing the keyword : ",keyword)

url_predictor = UrlPredect()
df = url_predictor.get_data_from_database()
responseBuilder = ResponseBuilder()  
nb_top = 10
nb_url = 100

responseBuilder.nb_url = nb_url
responseBuilder.nb_top = nb_top
responseBuilder.keyword = selected_keyword_index

print("printing the responseBuilder.nb_url", responseBuilder.nb_url)
print("printing the responseBuilder.nb_top", responseBuilder.nb_top)


dataframe =df
# Exclure et convertir les colonnes 
colonnes_exclues = ['Thekeyword','Url']
trainer = TrainModels()
df = df.drop(columns=colonnes_exclues, errors='ignore')
trainer.df = df

print("the dataframe to get train", trainer.df)



#Prétraitement de la data test
data= url_predictor.exclude_and_convert_columns(trainer.df)
trainer.df = data

print("test : ",trainer.df)


trainer.preprocessing()
X_train, X_test, y_train, y_test = trainer.split_data(trainer.X, trainer.y)
trained_model= trainer.train_XGBClassifier(X_train, y_train)
auc, acc = trainer.eval_model(trained_model,X_test, y_test)
print(auc, acc)


responseBuilder.trainedModels= trained_model
responseBuilder.trainedModels.X = X_train
responseBuilder.trainedModels.y = y_train
responseBuilder.df = dataframe


print("the responseBuilder", responseBuilder.trainedModels)
print("the responseBuilder.X",responseBuilder.trainedModels.X)
print("the responseBuilder.X",responseBuilder.trainedModels.y)


result  =responseBuilder.get_url_predect_result(specific_url, keyword)
print("Résultat :", result)


if url_predictor.url_data is None:
    print("url_predictor.url_data est None. Vérifiez l'initialisation.")

# Les colonnes que vous souhaitez conserver
columns_to_keep = responseBuilder.trainedModels.X.columns

# Identifiez les colonnes manquantes dans up.url_data
missing_columns = [col for col in columns_to_keep if col not in url_predictor.url_data.columns]

# Si des colonnes manquent, affichez un message ou émettez une exception
if missing_columns:
    print("Colonnes manquantes:", missing_columns)
    # Décider ce qu'il faut faire avec ces colonnes manquantes


result  =responseBuilder.get_url_predect_result(specific_url, keyword)
print("Résultat :", result)"""

<<<<<<< HEAD
=======
# Appeler la fonction try_for_columns avec le modèle entraîné pour prédir pour la donnée test 
result = url_predictor.try_for_columns(trained_model, response_builder)
print(result)
"""
>>>>>>> 380f5623e5454e10dcc670b83a03d4ff2b7896ab

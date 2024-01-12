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


"""# Initialisation de la classe TrainModels
trainer = TrainModels()

# Read data from Data Base
trainer.read_my_data()

# Accéder aux DataFrames créés par la méthode
trainer.df = trainer.data_to_drop(trainer.df)

# Prétraitement de la data
trainer.preprocessing()"""


"""dc = DataColector()
links = dc.get_all_urls_for_site("https://www.hyffen.com/agence")
print(links)
print("Nombre de liens :", len(links))"""



"**********************************************************************Analyse des données****************************************************************************************"
"""print(trainer.df.isnull().sum())
print(trainer.df.dtypes)


sns.countplot(x='Top10', data=trainer.df)
plt.title('Distribution of Top10')
plt.show()


# Display summary statistics
print(trainer.df.describe())

trainer.train_models(trainer.df)  # Train your models
trainer.display_feature_importance('RandomForestClassifier')
importance_scores = trainer.models['RandomForestClassifier'][3]['score']
# Identify features with low importance scores (e.g., threshold = 0.01)
low_importance_features = trainer.df.columns[importance_scores < 0.01]
print("Features with low importance:", low_importance_features)

# Suppression des colonnes inutiles


result = trainer.train_models(trainer.df)

if result is not None:
    # Display feature importance for RandomForestClassifier
    trainer.display_feature_importance('RandomForestClassifier')
else:
    print("Error occurred during training.")

trainer.display_feature_importance('RandomForestClassifier')"""






"""*********************************************************Testing récupération url site****************************************************************************"""

"""url_predictor = UrlPredect()
df = url_predictor.get_data_from_database()
dc = DataColector()


# Utilisez la méthode get_all_site_urls à partir de l'instance
start_url = "https://www.agence-naga.fr/expertise/webmarketing/referencement-naturel-seo-lyon/"
keyword = "agence seo nantes referencement44fr"
response_builder = ResponseBuilder()
print(df.columns)



all_site_urls = dc.get_all_site_urls(start_url, 3)
print(all_site_urls)
print("Nombre de liens :", len(all_site_urls))"""


trainer = TrainModels()
# Read data from Data Base
trainer.read_my_data()
result = trainer.df.loc[trainer.df['Thekeyword'] == 'agence seo']

# Affichage du résultat
print("reultat de hotel",result)

# Accéder aux DataFrames créés par la méthode
"""trainer.df = trainer.data_to_drop(trainer.df)
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


# Display the number of elements in each set
print("Number of elements in X_train:", X_train.shape[0])
print("Number of elements in y_train:", y_train.shape[0])
print("Number of elements in X_test:", X_test.shape[0])
print("Number of elements in y_test:", y_test.shape[0])
"""
"*************************Testing models**********************************"
"""stack_model, X_test_stack, y_test_stack, Model1, Model2, Model3, Model4, Model5= trainer.train_and_evaluate_stacking(X_train, y_train, X_test, y_test, n_folds=5)
auc, acc= trainer.eval_model(stack_model, X_test_stack, y_test_stack)
print(auc)
print("The accuracy",acc)


url_predictor = UrlPredect()
response_builder = ResponseBuilder()

df = url_predictor.get_data_from_database()

if not df.empty:
    num_columns = df.shape[1]
    print("Nombre de colonnes dans data_dr :", num_columns)

    specific_url = 'https://www.mintense.fr/'
    keyword = 'agence seo lille'


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
print(result)"""

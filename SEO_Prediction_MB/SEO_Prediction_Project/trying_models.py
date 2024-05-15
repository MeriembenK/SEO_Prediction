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


# Récupérer tous les mots-clés depuis la base de données
keywords = Keyword.objects.all()

# Afficher les options disponibles à l'utilisateur
print("Choisissez le mot-clé :")
for index, keyword in enumerate(keywords, start=1):
    print(f"{index}. {keyword.Keyword}")

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
response_builder.keyword = selected_keyword

# Prétraitement de la data
trainer.preprocessing()

pd.set_option('display.max_rows', None)
print(trainer.X.isnull().sum())


#Split data entre data d'entrainement et la data du test
"""X_train, X_test, y_train, y_test = trainer.split_data(trainer.X, trainer.y)

# Display the number of elements in each set
print("Number of elements in X_train:", X_train.shape[0])
print("Number of elements in y_train:", y_train.shape[0])
print("Number of elements in X_test:", X_test.shape[0])
print("Number of elements in y_test:", y_test.shape[0])"""

trainedModels, X_train, y_train, X_test, y_test=trainer.Final_get_importance()
response_builder.trainedModels = trainedModels

response_builder.trainedModels.X = X_train
response_builder.trainedModels.y = y_train

"*************************Testing models**********************************"
"""stack_model, X_test_stack, y_test_stack, Model1, Model2, Model3, Model4, Model5= trainer.train_and_evaluate_stacking(X_train, y_train, X_test, y_test, n_folds=5)
auc, acc= trainer.eval_model(stack_model, X_test_stack, y_test_stack)
print(auc)
print("The accuracy",acc)"""


df5 = response_builder.get_min_max()

print(df5)
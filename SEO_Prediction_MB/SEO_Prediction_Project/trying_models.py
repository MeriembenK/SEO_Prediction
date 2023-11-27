import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
django.setup() 

from Predictive.data_colector import DataColector 
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pandas as pd
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from fake_useragent import UserAgent
import random
from Predictive.train_Models import TrainModels
from tabulate import tabulate
import numpy as np




trainer = TrainModels()
#Read data from Data Base
trainer.read_my_data()
# Access the DataFrames created by the method
data_df = trainer.df
data_df = trainer.data_to_drop(data_df)
trainer.df = data_df
trainer.preprocessing()

# Step 5: Print or inspect the processed data
print("Processed DataFrame:")
print(trainer.df.head())
print("\nTarget Variable (y):")
print(trainer.y.head())
print("\nFeatures (X):")
print(trainer.X.head())

X = trainer.X
y = trainer.y

# Divisez les données
X_train, X_test, y_train, y_test = trainer.split_data(X, y)
print("Number of training data points:", X_train.shape[0])
print("Number of test data points:", X_test.shape[0])
print("Number of training target:", y_train.shape[0])
print("Number of test data points:", y_test.shape[0])

# Affichez les dimensions de vos données avant de commencer
print("Dimensions de X_train:", X_train.shape)
print("Dimensions de y_train:", y_train.shape)

"""************************************************************************TESTING STACKING***************************************************************************************"""
#testing Models
stacking_model, accuracy = trainer.train_and_evaluate_stacking(X_train, y_train, X_test, y_test)

print("Stacking's accuracy")
print(accuracy)


"""************************************************************************TESTING VOTING*****************************************************************************************"""

Voting_accuracy = trainer.train_evaluate_voting(X_train, y_train, X_test, y_test, voting='hard')
print("Voting's's accuracy")
print(accuracy)


"""model1 = trainer.train_XGBClassifier(X_train, y_train)
model2 =trainer.train_ExtraTreesClassifier(X_train, y_train)
model3 = trainer.train_RandomForestClassifier(X_train, y_train)
model4 = trainer.train_GradientBoostingClassifier(X_train, y_train)
model5 = trainer.train_AdaBoostClassifier(X_train, y_train)


# Faites des prédictions
#y_pred = trained_model.predict(X_test)

# Les prédictions
predictions = pd.DataFrame({
    'Model1': model1.predict(X_test),
    'Model2': model2.predict(X_test),
    'Model3': model3.predict(X_test),
    'Model4': model4.predict(X_test),
    'Model5': model5.predict(X_test),
    'Actual': y_test 
})

X_stack = predictions[['Model1', 'Model2', 'Model3', 'Model4', 'Model5']]
y_stack = predictions['Actual']

X_train_stack, X_test_stack, y_train_stack, y_test_stack = trainer.split_data(X_stack, y_stack)
stack_model = trainer.train_XGBClassifier(X_train, y_train)

stack_model.fit(X_train_stack, y_train_stack)
y_pred_stack = stack_model.predict(X_test_stack)

accuracy = accuracy_score(y_test_stack, y_pred_stack)
print("Accuracy:", accuracy)

precision = precision_score(y_test_stack, y_pred_stack)
print("Precision:", precision)


recall = recall_score(y_test_stack, y_pred_stack)
print("Recall:", recall)


f1 = f1_score(y_test_stack, y_pred_stack)
print("F1 Score:", f1)


conf_matrix = confusion_matrix(y_test_stack, y_pred_stack)
print("Confusion Matrix:\n", conf_matrix)"""

"""
# Affichez les dimensions de vos données de test après les prédictions
print("Dimensions de X_test après les prédictions:", X_test.shape)
print("Dimensions de y_pred:", y_pred.shape)


accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)


precision = precision_score(y_test, y_pred)
print("Precision:", precision)


recall = recall_score(y_test, y_pred)
print("Recall:", recall)


f1 = f1_score(y_test, y_pred)
print("F1 Score:", f1)


conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", conf_matrix)"""

"""
# Supposons que X_train est votre DataFrame
columns_with_nan = X_train.columns[X_train.isnull().any()].tolist()

print("Colonnes avec des valeurs NaN :", columns_with_nan)

# Supposons que X_train est votre DataFrame
pd.set_option('display.max_rows', None)  # Afficher toutes les lignes
pd.set_option('display.max_columns', None)  # Afficher toutes les colonnes

nan_count_per_column = X_train.isnull().sum()

print("Nombre de NaN par colonne :\n", nan_count_per_column)

# Remettre les options d'affichage par défaut si nécessaire
pd.reset_option('display.max_rows')
pd.reset_option('display.max_columns')"""
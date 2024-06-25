"""**************************************************************************MODELES DE MACHINE LEARNING**************************************************************************"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE 
from sklearn.model_selection import KFold
from SEO_Prediction_App.models import Data
import seaborn as sns
import matplotlib.pyplot as plt
from SEO_Prediction_App.models import Test
from django.utils import timezone

class TrainModels:


    #Initialisation de la classe TrainModel
    def __init__(self) :
        self.df = None
        self.X  = None
        self.y  = None
        self.X_over = None
        self.y_over = None
        self.models = None
        self.path   = None
        self.X_train_stack = None
        self.keyword= None

    def read_my_data_for_url(self):
        colonnes_exclues = ['id','Position','Url_Score', 'HTTP_Version','Http_code_babbar','Thekeyword','Content_type','Status_code','Status','Indexability_x','Indexability_status_x'
                            ,'X_robots_tag1','Meta_Robots_1_score','Meta_Refresh_1','Canonical_link_element1','rel_next_1','rel_prev_1','HTTP_rel_next_1','HTTP_rel_prev_1','amphtml_link_element',
                              'Readability','Link_score','Closest_Similarity_Match','NoNear_Duplicates','Spelling_Errors','Grammar_Errors','Hash','Last_modified','Redirect_URL',
                              'Redirect_type','Cookies','URL_Encoded_Address','Crawl_Timestamp','Type_1','Indexability_y','Indexability_Status_y', 'Date_added']
        toutes_colonnes = [f.name for f in Data._meta.get_fields()]
        colonnes_incluses = [nom_colonne for nom_colonne in toutes_colonnes if nom_colonne not in colonnes_exclues]
        
        # Filtrer les données avec Keyword=self.keyword
        data_queryset = Data.objects.all().values(*colonnes_incluses)
        self.df = pd.DataFrame.from_records(data_queryset) 
        self.df = self.df.convert_dtypes()
        
        float_columns = [ 'Ttfb_babbar', 'Page_value_babbar', 'Page_trust_babbar', 'Semantic_value_babbar', 'Backlinks_babbar', 'Backlinks_host_babbar'
                         , 'Host_outlinks_babbar', 'Outlinks_babbar', 'Desktop_first_contentful_paint_terrain', 'Desktop_cumulative_layout_shift_terrain', 'Desktop_first_contentful_paint_lab',
                         'Desktop_largest_contentful_paint_lab','Desktop_speed_index_lab', 'SOSEO_yourtext_guru', 'DSEO_yourtext_guru', 'Word_count', 'Sentence_Count', 'Flesch_reading_ease_score', 'H1_2_length',
                         'Crawl_depth', 'Inlinks', 'Unique_inlinks', 'H2_2_score', 'H2_1_score', 'H1_1_score', 'Meta_Keywords1_score', 'Meta_Description1_score', 'Total_Types',
                         'Warnings', 'Unique_External_JS_Outlinks', 'Unique_External_Outlinks', 'External_Outlinks', 'Unique_Outlinks', 'of_Total', 'Desktop_cumulative_layout_shift_lab',
                         'Desktop_largest_contentful_paint_terrain', 'Desktop_first_input_delay_terain', 'Desktop_time_to_interactive_lab', 'Outlinks', 'Title1_pixel_width', 'Title2', 'Title2_length', 'H1_1_length', 'H2_2_length',
                         'Title2_pixel_width', 'Meta_description1', 'Meta_description1_Pixel_width', 'Meta_description2', 'Meta_description2_length', 'Meta_keywords1_length', 'H2_1_length',
                           'Meta_description2_Pixel_width', 'Meta_Keywords1', 'H1_1','H1_2', 'H2_1', 'H2_2', 'Average_words_per_sentence', 'Response_time', 'Unique_JS_inlinks', 'Unique_JS_Outlinks', 'Errors', 
                           'Unique_Types', 'Meta_robots_1', 'Meta_robots_2', 'Meta_robots_3', 'Canonical_link_element2', 'Text_ratio']
        
        self.df[float_columns] = self.df[float_columns].apply(pd.to_numeric, errors='coerce')
        self.df[float_columns].fillna(0, inplace=True)
        
        columns_to_convert = ['H1_2_score','H2_2_score','H2_2', 'Size_bytes','Word_count','Sentence_Count','Inlinks','Mobile_first_contentful_paint_terrain', 'Mobile_first_input_delay_terain',
                              'Mobile_largest_contentful_paint_terrain', 'H2_1_score', 'H1_1_score', 'Meta_Keywords1_score', 'Meta_Description1_score', 'Title1_score', 'Unique_Types',
                               'Total_Types', 'Errors', 'Unique_External_JS_Outlinks', 'Unique_External_Outlinks', 'External_Outlinks', 'Unique_JS_Outlinks', 'Warnings', 'of_Total', 'Unique_JS_inlinks',
                                'Unique_inlinks', 'Crawl_depth', 'Flesch_reading_ease_score', 'Average_words_per_sentence', 'Meta_description1_Pixel_width', 'Title1_pixel_width', 'DSEO_yourtext_guru',
                                'SOSEO_yourtext_guru', 'Desktop_cumulative_layout_shift_lab', 'Desktop_largest_contentful_paint_lab', 'Desktop_first_contentful_paint_lab', 'Title1', 'Title1_length', 
                                'Desktop_cumulative_layout_shift_terrain', 'Desktop_largest_contentful_paint_terrain', 'Desktop_first_input_delay_terain', 'Desktop_first_contentful_paint_terrain',
                                'Outlinks_babbar', 'Host_outlinks_babbar', 'Backlinks_host_babbar', 'Backlinks_babbar', 'Semantic_value_babbar', 'Page_trust_babbar', 'Page_value_babbar', 'Ttfb_babbar',
                               'Desktop_total_blocking_time_lab','Outlinks','Mobile_cumulative_layout_shift_terrain', 'Mobile_first_contentful_paint_lab', 'Mobile_cumulative_layout_shift_lab',
                               'Mobile_speed_index_lab', 'Mobile_largest_contentful_paint_lab','Unique_Outlinks', 'Mobile_time_to_interactive_lab', 'Mobile_total_blocking_time_lab', 'Score_1fr',
                               'Meta_description1_length', 'Text_ratio' ]
        
        for column in columns_to_convert:
            # Conversion en float avec gestion des colonnes catégoriques
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce', downcast='float')
            if pd.api.types.is_categorical_dtype(self.df[column]):
                self.df[column] = pd.to_numeric(self.df[column], errors='coerce', downcast='float')

        return self.df
    #Lecture de la data depuis la BDD, en ignorant certaines colonnes, en faisant la conversion de certaines colonne de type object au type float et gestion des colonnes catégoriques
    def read_my_data(self):

        colonnes_exclues = ['id','Position','Url_Score', 'HTTP_Version','Http_code_babbar','Thekeyword','Content_type','Status_code','Status','Indexability_x','Indexability_status_x'
                              ,'X_robots_tag1','Meta_Robots_1_score','Meta_Refresh_1','Canonical_link_element1','rel_next_1','rel_prev_1','HTTP_rel_next_1','HTTP_rel_prev_1','amphtml_link_element',
                              'Readability','Link_score','Closest_Similarity_Match','NoNear_Duplicates','Spelling_Errors','Grammar_Errors','Hash','Last_modified','Redirect_URL',
                              'Redirect_type','Cookies','URL_Encoded_Address','Crawl_Timestamp','Type_1','Indexability_y','Indexability_Status_y', 'Date_added']
        toutes_colonnes = [f.name for f in Data._meta.get_fields()]
        colonnes_incluses = [nom_colonne for nom_colonne in toutes_colonnes if nom_colonne not in colonnes_exclues]
        data_queryset = Data.objects.filter(Keyword=self.keyword).values(*colonnes_incluses)
        self.df = pd.DataFrame.from_records(data_queryset) 
        self.df = self.df.convert_dtypes()
        
        float_columns = [ 'Ttfb_babbar', 'Page_value_babbar', 'Page_trust_babbar', 'Semantic_value_babbar', 'Backlinks_babbar', 'Backlinks_host_babbar'
                         , 'Host_outlinks_babbar', 'Outlinks_babbar', 'Desktop_first_contentful_paint_terrain', 'Desktop_cumulative_layout_shift_terrain', 'Desktop_first_contentful_paint_lab',
                         'Desktop_largest_contentful_paint_lab','Desktop_speed_index_lab', 'SOSEO_yourtext_guru', 'DSEO_yourtext_guru', 'Word_count', 'Sentence_Count', 'Flesch_reading_ease_score', 'H1_2_length',
                         'Crawl_depth', 'Inlinks', 'Unique_inlinks', 'H2_2_score', 'H2_1_score', 'H1_1_score', 'Meta_Keywords1_score', 'Meta_Description1_score', 'Total_Types',
                         'Warnings', 'Unique_External_JS_Outlinks', 'Unique_External_Outlinks', 'External_Outlinks', 'Unique_Outlinks', 'of_Total', 'Desktop_cumulative_layout_shift_lab',
                         'Desktop_largest_contentful_paint_terrain', 'Desktop_first_input_delay_terain', 'Desktop_time_to_interactive_lab', 'Outlinks', 'Title1_pixel_width', 'Title2', 'Title2_length', 'H1_1_length', 'H2_2_length',
                         'Title2_pixel_width', 'Meta_description1', 'Meta_description1_Pixel_width', 'Meta_description2', 'Meta_description2_length', 'Meta_keywords1_length', 'H2_1_length',
                           'Meta_description2_Pixel_width', 'Meta_Keywords1', 'H1_1','H1_2', 'H2_1', 'H2_2', 'Average_words_per_sentence', 'Response_time', 'Unique_JS_inlinks', 'Unique_JS_Outlinks', 'Errors', 
                           'Unique_Types', 'Meta_robots_1', 'Meta_robots_2', 'Meta_robots_3', 'Canonical_link_element2', 'Text_ratio']
        
        self.df[float_columns] = self.df[float_columns].apply(pd.to_numeric, errors='coerce')
        self.df[float_columns].fillna(0, inplace=True)
        
        columns_to_convert = ['H1_2_score','H2_2_score','H2_2', 'Size_bytes','Word_count','Sentence_Count','Inlinks','Mobile_first_contentful_paint_terrain', 'Mobile_first_input_delay_terain',
                              'Mobile_largest_contentful_paint_terrain', 'H2_1_score', 'H1_1_score', 'Meta_Keywords1_score', 'Meta_Description1_score', 'Title1_score', 'Unique_Types',
                               'Total_Types', 'Errors', 'Unique_External_JS_Outlinks', 'Unique_External_Outlinks', 'External_Outlinks', 'Unique_JS_Outlinks', 'Warnings', 'of_Total', 'Unique_JS_inlinks',
                                'Unique_inlinks', 'Crawl_depth', 'Flesch_reading_ease_score', 'Average_words_per_sentence', 'Meta_description1_Pixel_width', 'Title1_pixel_width', 'DSEO_yourtext_guru',
                                'SOSEO_yourtext_guru', 'Desktop_cumulative_layout_shift_lab', 'Desktop_largest_contentful_paint_lab', 'Desktop_first_contentful_paint_lab', 'Title1', 'Title1_length', 
                                'Desktop_cumulative_layout_shift_terrain', 'Desktop_largest_contentful_paint_terrain', 'Desktop_first_input_delay_terain', 'Desktop_first_contentful_paint_terrain',
                                'Outlinks_babbar', 'Host_outlinks_babbar', 'Backlinks_host_babbar', 'Backlinks_babbar', 'Semantic_value_babbar', 'Page_trust_babbar', 'Page_value_babbar', 'Ttfb_babbar',
                               'Desktop_total_blocking_time_lab','Outlinks','Mobile_cumulative_layout_shift_terrain', 'Mobile_first_contentful_paint_lab', 'Mobile_cumulative_layout_shift_lab',
                               'Mobile_speed_index_lab', 'Mobile_largest_contentful_paint_lab','Unique_Outlinks', 'Mobile_time_to_interactive_lab', 'Mobile_total_blocking_time_lab', 'Score_1fr',
                               'Meta_description1_length', 'Text_ratio' ]
        
        for column in columns_to_convert:

            #print("Converting column:", column)
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce', downcast='float')
            #print(self.df.dtypes)
            if pd.api.types.is_categorical_dtype(self.df[column]):
        # Gérer les colonnes catégoriques
             self.df[column] = pd.to_numeric(self.df[column], errors='coerce', downcast='float')

        return self.df
             

    def replace_underscore_with_space(self, input_string):
      # Ajoute "_score" à la fin de la chaîne de caractères
       output_string = input_string + '_score'
       return output_string

    #Suppression de certaines colonnes inutiles
    def data_to_drop(self,df):
               
        df = df.loc[:, df.isin([' ','NULL' ]).mean(axis=0) < .6]
        return df
    


    #Prétraitement des données, remplacement des nan par 0 ou la moyenne
    def preprocessing(self):
        df = self.df
        
        # Remplacer les valeurs manquantes dans les colonnes spécifiques par zéro
        columns_to_replace = ['Title1_length', 'Title2_length', 'Title2_pixel_width', 'Desktop_total_blocking_time_lab', 'Title1', 
                              'Title2', 'Meta_description2', 'Meta_Keywords1', 'H1_1', 'H1_2', 'H2_1', 'H2_2', 'Meta_robots_1',
                                'Meta_robots_2', 'Meta_robots_3', 'Canonical_link_element2', 'Meta_description1', 'Meta_description1_length',
                                  'H1_1_length', 'H2_1_length', 'H2_2_length', 'Size_bytes', 'Word_count', 'Sentence_Count', 'Inlinks', 'Outlinks',
                                    'Unique_Outlinks', 'External_Outlinks', 'Unique_External_Outlinks', 'SOSEO_yourtext_guru', 'DSEO_yourtext_guru', 'Score_1fr']
        df[columns_to_replace] = df[columns_to_replace].fillna(0)

        # Sélectionner uniquement les colonnes numériques
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        # Remplacer les valeurs manquantes dans les colonnes numériques par leur moyenne
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

        self.df = df
        self.y = df['Top10'] 
        self.X = df.drop(['Top10'], axis=1).copy()



    #Diviser la data entre, données d'entrainement et données de test
    def split_data(self,X,y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2,random_state=42)
        return X_train, X_test, y_train, y_test
    


    # 1 premier model 
    def train_XGBClassifier(self,X_train,y_train):
        parameters = {
            "learning_rate": np.arange(0.01, 0.1, 0.01),
            "n_estimators": np.arange(100, 1000, 100),
            "max_depth": np.arange(3, 10, 1),
            "min_child_weight": np.arange(1, 5, 1),
        }
        model = XGBClassifier( random_state=42)
        model.fit(X_train, y_train)
        model.X_train = X_train  # Ajoutez cet attribut
        model.y_train = y_train  # Ajoutez cet attribut
        print("*****************************************************************Train model 1 : XGBClassifier*****************************************************************")
        return model
    



    # 2 deuxiem modele
    def train_ExtraTreesClassifier(self,X_train,y_train):
        model = ExtraTreesClassifier( random_state=42)
        model.fit(X_train, y_train)
        print("****************************************************************Train model 2 : ExtraTreesClassifier**********************************************************")
        return model
    



    # 3 troisieme modele
    def train_RandomForestClassifier(self,X_train,y_train):
        # Create the parameter grid
        param_grid = {
            'n_estimators': [10, 100, 1000],
            'max_depth': [3, 5, 10],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 5],
        }
        model = RandomForestClassifier( random_state=42)
        model.fit(X_train, y_train)
        print("****************************************************************Train model 3 : RandomForestClassifier*******************************************************")
        return model
    



     # 4 quatrième modele
    def train_GradientBoostingClassifier(self,X_train,y_train):
        model = GradientBoostingClassifier( random_state=42)
        model.fit(X_train, y_train)
        print("*****************************************************************Train model 4 : GradientBoostingClassifier**************************************************")
        return model
    



    # 5 cinquième modele
    def train_AdaBoostClassifier(self,X_train,y_train):
        model = AdaBoostClassifier( random_state=42)
        model.fit(X_train, y_train)
        print("*****************************************************************Train model 5 : AdaBoostClassifier***********************************************************")
        return model
    


        #Evaluation du modele en retournant l'accuracy et l'auc
    def eval_model(self,model,X_test,y_test):
        num_data_test = X_test.shape[0]
        y_predect = model.predict(X_test)
        auc = roc_auc_score(y_test, y_predect)
        acc = accuracy_score(y_test, y_predect)
        conf_matrix = confusion_matrix(y_test, y_predect)
    
        # Affichage de la matrice de confusion avec seaborn
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Top10', 'Non Top10'], yticklabels=['Top10', ' Non Top10'])
        return auc , acc       



    #Methode ensembliste
    #Stacking
    def train_and_evaluate_stacking(self, X_train, y_train, X_test, y_test,  n_folds=5):
     # Entraînez les modèles individuels
      models = {}
      model1,auc, acc, importance_score = self.train_model_kFold(self.train_XGBClassifier)
      models.update({'XGBClassifier': [model1, auc, acc, importance_score]})
      print("20%")

      print("The AUC model1 : XGBClassifier ",auc)
      print("The ACC model1 : XGBClassifier",acc)

      model2,auc, acc, importance_score = self.train_model_kFold(self.train_ExtraTreesClassifier)
      models.update({'ExtraTreesClassifier': [model2, auc, acc, importance_score]})
      print("40%")

      print("The AUC model2 : ExtraTreesClassifier",auc)
      print("The ACC model2 : ExtraTreesClassifier",acc)

      model3,auc, acc, importance_score = self.train_model_kFold(self.train_RandomForestClassifier)
      models.update({'RandomForestClassifier': [model3, auc, acc, importance_score]})
      print("60%")

      print("The AUC model3 : RandomForestClassifier",auc)
      print("The ACC model3 : RandomForestClassifier",acc)

      model4, auc, acc, importance_score = self.train_model_kFold(self.train_GradientBoostingClassifier)
      models.update({'GradientBoostingClassifier': [model4, auc, acc, importance_score]})
      print("80%")

      print("The AUC model4 : GradientBoostingClassifier",auc)
      print("The ACC model4 : GradientBoostingClassifier",acc)

      model5, auc, acc, importance_score = self.train_model_kFold(self.train_AdaBoostClassifier)
      models.update({'AdaBoostClassifier': [model5, auc, acc, importance_score]})
      print("100%")


      print("The AUC model5 : AdaBoostClassifier",auc)
      print("The ACC model6 : AdaBoostClassifier",acc)
    
    # Faites des prédictions de probabilité avec les modèles individuels
      predictions = pd.DataFrame({
            'Model1': cross_val_predict(model1, X_test, y_test, cv=n_folds, method='predict_proba')[:, 1],
            'Model2': cross_val_predict(model2, X_test, y_test, cv=n_folds, method='predict_proba')[:, 1],
            'Model3': cross_val_predict(model3, X_test, y_test, cv=n_folds, method='predict_proba')[:, 1],
            'Model4': cross_val_predict(model4, X_test, y_test, cv=n_folds, method='predict_proba')[:, 1],
            'Model5': cross_val_predict(model5, X_test, y_test, cv=n_folds, method='predict_proba')[:, 1],
            'Actual': y_test
        })
      print("Shape of X_test:", X_test.shape)
      print("Shape of predictions:", predictions.shape)

     # Créez les données d'entrée pour le modèle de stacking
      X_stack = predictions[['Model1', 'Model2', 'Model3', 'Model4', 'Model5']].copy()
      y_stack = predictions['Actual']

      print("Shape of X_stack:", X_stack.shape)
      print("Shape of y_stack:", y_stack.shape)

      X_train_stack, X_test_stack, y_train_stack, y_test_stack = self.split_data(X_stack, y_stack)
     # Entraînez le modèle de stacking
      stack_model = self.train_XGBClassifier(X_train_stack, y_train_stack)
      self.X_train_stack = X_train_stack
      self.models = models
      return stack_model,X_test_stack, y_test_stack, model1, model2, model3, model4, model5
    
    
    def Final_get_importance(self, user_instance): 
        test_instance = Test()
        test_instance = Test(user=user_instance)

        test_instance.Keyword = self.keyword
        test_instance.nb_url = self.df.shape[0]
        X_train, y_train, X_test, y_test = self.oversampling_Smote()
        print("nb ligne de trainer.df est ", self.df.shape[0])
        stack_model, X_test_stack, y_test_stack, Model1, Model2, Model3, Model4, Model5 = self.train_and_evaluate_stacking(X_train, y_train, X_test, y_test, n_folds=5)
        auc, acc = self.eval_model(stack_model, X_test_stack, y_test_stack)
        print(auc)
        print("The accuracy", acc)
        test_instance.precision = acc

        df_importance = self.get_importance_level1(stack_model)
        print(df_importance)

        # Triez le DataFrame par score en ordre décroissant
        df_sorted = df_importance.sort_values(by='score', ascending=False)

        # Obtenez le nom du modèle avec le score le plus élevé
        best_model_name = df_sorted.iloc[0]['variable']

        if best_model_name == 'Model1':
            df_model = self.get_importance(Model1)
        elif best_model_name == 'Model2':
            df_model = self.get_importance(Model2)
        elif best_model_name == 'Model3':
            df_model = self.get_importance(Model3)
        elif best_model_name == 'Model4':
            df_model = self.get_importance(Model4)
        elif best_model_name == 'Model5':
            df_model = self.get_importance(Model5)
        else:
            # Gérez le cas où best_model_name n'est pas l'un des modèles connus
            raise ValueError("Nom de modèle inconnu")

        print("Attributs de la classe Test :", dir(Test))

        for variable, score in zip(df_model['variable'], df_model['score']):
            #print(f"Variable : {variable}, Score : {score}")
            variable_with_spaces = self.replace_underscore_with_space(variable)  # Passer variable comme argument
            # Assurez-vous que le nom de la variable correspond à un attribut de la classe Test
            if hasattr(test_instance, variable_with_spaces):
                # Assurez-vous que la colonne 'variable' est une colonne valide de la classe Test
                setattr(test_instance, variable_with_spaces, score)
            else:
                print(f"La variable {variable_with_spaces} n'est pas un attribut de la classe Test.")

        # Assignez la date et l'heure actuelles
        current_time = timezone.now()
        test_instance.date_test = current_time.date()
        test_instance.hour_test = current_time.time()
        test_instance.save()
        
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        # Affichez le DataFrame
        print(df_model)
        return stack_model, X_train, y_train, X_test, y_test

     
   
    def grid_search(self ,X, y,param_grid,fun):
        # Create the grid search object
        grid_search = GridSearchCV(
            estimator=fun,
            param_grid=param_grid,
            cv=5, 
            scoring="roc_auc"
        )
        # Fit the grid search object
        grid_search.fit(X, y)

        # Return the best model
        return grid_search.best_estimator_
    
    #Pour améliorer la performance lorsqu'on a un désiquilibre entre les classes pour evité que le modèle soit biaisé vers la classe majoritaire
    def oversampling_Smote(self):
        X_train, X_test, y_train, y_test = self.split_data(self.X,self.y)
        oversample = SMOTE(random_state=42, sampling_strategy='auto')
        X_train, y_train = oversample.fit_resample( X_train, y_train )
        print("Type de y_train avant conversion:", y_train.dtypes)
        y_train = y_train.astype(int)  
        print("Type de y_train après conversion:", y_train.dtypes)
        return X_train, y_train, X_test, y_test

    


    #entrainement d'un modele
    def train_model(self,fun, **kwargs):
        
        X_train, X_test, y_train, y_test = self.split_data(self.X,self.y)
        
        oversample = SMOTE(random_state=42, sampling_strategy='auto')
        X_train, y_train = oversample.fit_resample( X_train, y_train )

        model = fun(X_train,y_train)
        auc , acc = self.eval_model(model,X_test,y_test)
        importance_score = self.get_importance(model)
        return model , auc , acc , importance_score




    #entrainement des modele de base (les 5 modeles, un par un)
    def train_model_level1(self,model, X_train, y_train, X_test, y_test):
        
        auc , acc = self.eval_model(model,X_test,y_test)
        importance_score = self.get_importance(model)
        return model , auc , acc , importance_score



    #Avoir un classement des colonnes de la dataframe par ordre croissant d'importance dans l'entrainement
    def get_importance_level1(self, model):
      # Obtenez les scores d'importance des fonctionnalités du modèle
       importance_scores = model.feature_importances_

        # Obtenez le nom des fonctionnalités à partir des colonnes de X_train_stack
       feature_names = self.X_train_stack.columns

    # Créez un DataFrame trié avec les noms de fonctionnalités et les scores d'importance
       df_scores = pd.DataFrame(data={'variable': feature_names, 'score': importance_scores})
       df_sorted = df_scores.sort_values(by='score', ascending=False)

       first_row = df_sorted.iloc[0]
       return df_sorted 
    


    
    def get_importance(self,model):
        
        list_col = list(self.X.columns)
        importance = model.feature_importances_
        # summarize feature importance
        list_score = []
        for i,v in enumerate(importance):
            list_score.append(v)
        print("Length of list_score:", len(list_score))
        df_scores = pd.DataFrame(data={'variable':list_col,'score':list_score})
        df_sorted = df_scores.sort_values(by=['score'],ascending=False)

        return df_sorted
    
    
    def display_feature_importance(self, model_name):
        if self.models is None or not isinstance(self.models, dict):
            print("Models have not been trained.")
            return

        if model_name not in self.models:
            print(f"Model {model_name} not found.")
            return

        model_info = self.models[model_name]
        model = model_info[0]

        if hasattr(model, 'feature_importances_'):
            feature_names = self.X.columns
            importance_scores = model.feature_importances_

            feature_importance = pd.DataFrame(
                {'Feature': feature_names, 'Importance': importance_scores}
            ).sort_values(by='Importance', ascending=False)

            print(f"Feature importance for {model_name}:")
            print(feature_importance)

        else:
            print(f"Model {model_name} does not provide feature importance information.")


    # Fonction de validation croisée avec suréchantillionage pour entrainer et valider les modèles 
    def train_model_kFold(self,fun):
        
        kf = KFold(n_splits=5)
        X_train, X_valid, y_train, y_valid = self.split_data(self.X,self.y)
        auc_init = 0
        best_model = None
        for  train_index, test_index  in  kf.split(X_train):
            try:
                 
                #print('123')
                X_train_Kfold, X_test_Kfold = X_train.iloc[train_index], X_train.iloc[test_index]
                y_train_Kfold, y_test_Kfold = y_train.iloc[train_index], y_train.iloc[test_index]

                oversample = SMOTE(random_state=42)
                X_train_over, y_train_over = oversample.fit_resample( X_train_Kfold, y_train_Kfold )
    
                model = fun(X_train_over,y_train_over)
                auc , acc = self.eval_model(model,X_test_Kfold,y_test_Kfold)
                 
                if auc_init<auc:
                    best_model = model
            except Exception as e:
                print(e)
                pass

        auc , acc = self.eval_model(best_model,X_valid,y_valid)

        importance_score = self.get_importance(best_model)
        return best_model , auc , acc , importance_score
    



    def train_models(self, df):
        try:
            self.df = self.data_to_drop(df)
            self.preprocessing()
            models = {}

            # Train XGBClassifier
            model, auc, acc, importance_score = self.train_model_kFold(self.train_XGBClassifier)
            models.update({'XGBClassifier': [model, auc, acc, importance_score]})
            print("20%")

            # Train ExtraTreesClassifier
            model, auc, acc, importance_score = self.train_model_kFold(self.train_ExtraTreesClassifier)
            models.update({'ExtraTreesClassifier': [model, auc, acc, importance_score]})
            print("40%")

            # Train RandomForestClassifier
            model, auc, acc, importance_score = self.train_model_kFold(self.train_RandomForestClassifier)
            models.update({'RandomForestClassifier': [model, auc, acc, importance_score]})
            print("60%")

            # Train GradientBoostingClassifier
            model, auc, acc, importance_score = self.train_model_kFold(self.train_GradientBoostingClassifier)
            models.update({'GradientBoostingClassifier': [model, auc, acc, importance_score]})
            print("80%")

            # Train AdaBoostClassifier
            model, auc, acc, importance_score = self.train_model_kFold(self.train_AdaBoostClassifier)
            models.update({'AdaBoostClassifier': [model, auc, acc, importance_score]})
            print("100%")

            self.models = models
            return self  # Retourne l'instance de la classe
        except Exception as e:
           # Gère les erreurs ici, par exemple, imprime l'erreur
           print(f"An error occurred during training: {str(e)}")
           return None
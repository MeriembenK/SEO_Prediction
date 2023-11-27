import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, precision_score

 
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import VotingClassifier
from sklearn import metrics
# check version number
from imblearn.over_sampling import SMOTE 
from sklearn.model_selection import KFold
from SEO_Prediction_App.models import Data


class TrainModels:
    def __init__(self) :
        self.df = None
        self.X  = None
        self.y  = None
        self.X_over = None
        self.y_over = None
        self.models = None
        self.path   = None


    def read_my_data(self):
        colonnes_exclues = ['Position','Url_Score', 'HTTP_Version','Http_code_babbar','Thekeyword','Url','Content_type','Status_code','Status','Indexability_x','Indexability_status_x'
                            ,'X_robots_tag1','Meta_Robots_1_score','Meta_Refresh_1','Canonical_link_element1','rel_next_1','rel_prev_1','HTTP_rel_next_1','HTTP_rel_prev_1','amphtml_link_element',
                              'Readability','Link_score','Closest_Similarity_Match','NoNear_Duplicates','Spelling_Errors','Grammar_Errors','Hash','Last_modified','Redirect_URL',
                              'Redirect_type','Cookies','URL_Encoded_Address','Crawl_Timestamp','Type_1','Indexability_y','Indexability_Status_y', 'Date_added']
        toutes_colonnes = [f.name for f in Data._meta.get_fields()]
        colonnes_incluses = [nom_colonne for nom_colonne in toutes_colonnes if nom_colonne not in colonnes_exclues]
        data_queryset = Data.objects.all().values(*colonnes_incluses)
        self.df = pd.DataFrame.from_records(data_queryset) 
        self.df = self.df.convert_dtypes()
        
        float_columns = [ 'Ttfb_babbar', 'Page_value_babbar', 'Page_trust_babbar', 'Semantic_value_babbar', 'Backlinks_babbar', 'Backlinks_host_babbar'
                         , 'Host_outlinks_babbar', 'Outlinks_babbar', 'Desktop_first_contentful_paint_terrain', 'Desktop_cumulative_layout_shift_terrain', 'Desktop_first_contentful_paint_lab',
                         'Desktop_largest_contentful_paint_lab', 'SOSEO_yourtext_guru', 'DSEO_yourtext_guru', 'Word_count', 'Sentence_Count', 'Flesch_reading_ease_score', 'H1_2_length',
                         'Crawl_depth', 'Inlinks', 'Unique_inlinks', 'H2_2_score', 'H2_1_score', 'H1_1_score', 'Meta_Keywords1_score', 'Meta_Description1_score', 'Total_Types',
                         'Warnings', 'Unique_External_JS_Outlinks', 'Unique_External_Outlinks', 'External_Outlinks', 'Unique_Outlinks', 'of_Total', 'Desktop_cumulative_layout_shift_lab',
                         'Desktop_largest_contentful_paint_terrain', 'Desktop_first_input_delay_terain', 'Outlinks', 'Title1_pixel_width', 'Title2', 'Title2_length', 'H1_1_length', 'H2_2_length',
                         'Title2_pixel_width', 'Meta_description1', 'Meta_description1_Pixel_width', 'Meta_description2', 'Meta_description2_length', 'Meta_keywords1_length', 'H2_1_length',
                           'Meta_description2_Pixel_width', 'Meta_Keywords1', 'H1_1','H1_2', 'H2_1', 'H2_2', 'Average_words_per_sentence', 'Unique_JS_inlinks', 'Unique_JS_Outlinks', 'Errors', 
                           'Unique_Types', 'Meta_robots_1', 'Meta_robots_2', 'Meta_robots_3', 'Canonical_link_element2', 'Text_ratio', 'Response_time']
        
        self.df[float_columns] = self.df[float_columns].apply(pd.to_numeric, errors='coerce')
        self.df[float_columns].fillna(0, inplace=True)
        #certaines données sont reconnues comme type object alors qu'il sont float cela est du aux none

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

            print("Converting column:", column)
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce', downcast='float')
            print(self.df.dtypes)
            if pd.api.types.is_categorical_dtype(self.df[column]):
        # Gérer les colonnes catégoriques
             self.df[column] = pd.to_numeric(self.df[column], errors='coerce', downcast='float')

    def data_to_drop(self,df):
               
        df = df.loc[:, df.isin([' ','NULL' ]).mean(axis=0) < .6]
        return df
    
    def preprocessing(self):
        
        df = self.df
               
        print("Column names:", df.columns)
        print("DataFrame shape:", df.shape)
        print("Top10 column:", df['Top10'])


        print(df.shape)
        print(df['Top10'])
       
        df['Title1_length'             ].replace( np.nan,0, inplace=True)
        df['Desktop_total_blocking_time_lab'].replace( np.nan,0, inplace=True)
        df['Title1'             ].replace( np.nan,0, inplace=True)
        df['Title2'             ].replace( np.nan,0, inplace=True)
        df['Meta_description2'             ].replace( np.nan,0, inplace=True)
        df['Meta_Keywords1'             ].replace( np.nan,0, inplace=True)
        df['H1_1'             ].replace( np.nan,0, inplace=True)
        df['H1_2'             ].replace( np.nan,0, inplace=True)
        df['H2_1'             ].replace( np.nan,0, inplace=True)
        df['Meta_robots_1'             ].replace( np.nan,0, inplace=True)
        df['Meta_robots_2'             ].replace( np.nan,0, inplace=True)
        df['Meta_robots_3'             ].replace( np.nan,0, inplace=True)
        df['Canonical_link_element2'             ].replace( np.nan,0, inplace=True)
        df['Meta_description1'             ].replace( np.nan,0, inplace=True)
        df['Meta_description1_length'  ].replace( np.nan,0, inplace=True)
        df['H1_1_length'                ].replace( np.nan,0, inplace=True)
        df['H2_1_length'                ].replace( np.nan,0, inplace=True)
        df['H2_2_length'                ].replace( np.nan,0, inplace=True)
        df['Size_bytes'               ].replace( np.nan,0, inplace=True)
        df['Word_count'                 ].replace( np.nan,0, inplace=True)
        df['Sentence_Count'             ].replace( np.nan,0, inplace=True)
        df['Inlinks'                    ].replace( np.nan,0, inplace=True)
        df['Outlinks'                   ].replace( np.nan,0, inplace=True)
        df['Unique_Outlinks'            ].replace( np.nan,0, inplace=True)
        df['External_Outlinks'          ].replace( np.nan,0, inplace=True)
        df['Unique_External_Outlinks'   ].replace( np.nan,0, inplace=True)
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())


        self.df = df
        self.y = df['Top10'] 
        self.X = df.drop(['Top10'], axis=1).copy()


    
    def split_data(self,X,y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2,random_state=42)
        return X_train, X_test, y_train, y_test


    def eval_model(self,model,X_test,y_test):
        y_predect = model.predict(X_test)
        auc = roc_auc_score(y_test, y_predect)
        acc = accuracy_score(y_test, y_predect)
        return auc , acc       
    

    def get_importance(self,model):
        list_col = list(self.X.columns)
        importance = model.feature_importances_
        # summarize feature importance
        list_score = []
        for i,v in enumerate(importance):
            list_score.append(v)
        df_scores = pd.DataFrame(data={'variable':list_col,'score':list_score})
        df_sorted = df_scores.sort_values(by=['score'],ascending=False)
        return df_sorted
    

    # 1
    def train_XGBClassifier(self,X_train,y_train):
        parameters = {
            "learning_rate": np.arange(0.01, 0.1, 0.01),
            "n_estimators": np.arange(100, 1000, 100),
            "max_depth": np.arange(3, 10, 1),
            "min_child_weight": np.arange(1, 5, 1),
        }
        model = XGBClassifier( random_state=42)
        #best_model = self.grid_search(X_train,y_train,parameters,model)
        model.fit(X_train, y_train)
        return model
    

    # 2 
    def train_ExtraTreesClassifier(self,X_train,y_train):
        model = ExtraTreesClassifier( random_state=42)
        model.fit(X_train, y_train)
        return model
    

    # 3
    def train_RandomForestClassifier(self,X_train,y_train):
        # Create the parameter grid
        param_grid = {
            'n_estimators': [10, 100, 1000],
            'max_depth': [3, 5, 10],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 5],
        }
        model = RandomForestClassifier( random_state=42)
        #best_model = self.grid_search(X_train,y_train,param_grid,model)
        model.fit(X_train, y_train)
        return model
    

     # 4
    def train_GradientBoostingClassifier(self,X_train,y_train):
        model = GradientBoostingClassifier( random_state=42)
        model.fit(X_train, y_train)
        return model
    

    # 5
    def train_AdaBoostClassifier(self,X_train,y_train):
        model = AdaBoostClassifier( random_state=42)
        model.fit(X_train, y_train)
        return model
    
    #Methode ensembliste
    def train_and_evaluate_stacking(self, X_train, y_train, X_test, y_test):
     # Entraînez les modèles individuels
      model1 = self.train_XGBClassifier(X_train, y_train)
      model2 = self.train_ExtraTreesClassifier(X_train, y_train)
      model3 = self.train_RandomForestClassifier(X_train, y_train)
      model4 = self.train_GradientBoostingClassifier(X_train, y_train)
      model5 = self.train_AdaBoostClassifier(X_train, y_train)

     # Faites des prédictions avec les modèles individuels
      predictions = pd.DataFrame({
        'Model1': model1.predict(X_test),
        'Model2': model2.predict(X_test),
        'Model3': model3.predict(X_test),
        'Model4': model4.predict(X_test),
        'Model5': model5.predict(X_test),
        'Actual': y_test
       })

     # Créez les données d'entrée pour le modèle de stacking
      X_stack = predictions[['Model1', 'Model2', 'Model3', 'Model4', 'Model5']]
      y_stack = predictions['Actual']

     # Divisez les données pour le modèle de stacking
      X_train_stack, X_test_stack, y_train_stack, y_test_stack = self.split_data(X_stack, y_stack)

     # Entraînez le modèle de stacking
      stack_model = self.train_XGBClassifier(X_train_stack, y_train_stack)

     # Faites des prédictions avec le modèle de stacking
      y_pred_stack = stack_model.predict(X_test_stack)
      accuracy = accuracy_score(y_test_stack, y_pred_stack)
      print("Accuracy:", accuracy)
      return stack_model, accuracy
    


    def train_evaluate_voting(self, X_train, y_train, X_test, y_test, voting='hard'):
 
      models = [('XGB', XGBClassifier(random_state=42)),
          ('ExtraTrees', ExtraTreesClassifier(random_state=42)),
          ('RandomForest', RandomForestClassifier(random_state=42)),
          ('GradientBoosting', GradientBoostingClassifier(random_state=42)),
          ('AdaBoost', AdaBoostClassifier(random_state=42))]
        
      # Création du VotingClassifier
      voting_clf = VotingClassifier(estimators=models, voting=voting)

      # Entraînement du VotingClassifier sur les données d'entraînement
      voting_clf.fit(X_train, y_train)

      # Prédiction sur les données de test
      y_pred = voting_clf.predict(X_test)

      # Évaluation de la performance
      accuracy = accuracy_score(y_test, y_pred)
      print(f'Accuracy: {accuracy:.4f}')
      return accuracy


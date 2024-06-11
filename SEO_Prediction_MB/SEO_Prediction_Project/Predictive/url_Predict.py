"""*****************************************************************URL PREDICT*****************************************************************************************"""

from .SemantiqueValues import SemantiqueValues
from .data_colector import DataColector 
from SEO_Prediction_App.models import Data, Data_Url
from itertools import combinations
import pandas as pd
import numpy as np

class UrlPredect:

    #Constructeur de la classr UrlPredect
    def __init__(self) :
        self.url        = ''
        self.keyword    = ''
        self.url_data   = None
        self.url_data2  = None


     #Exclusion et conversion de certaines colonnes
    @staticmethod
    def exclude_and_convert_columns(data_frame):
        
        colonnes_exclues = ['id','Position','Url_Score', 'HTTP_Version','Http_code_babbar','Thekeyword','Content_type','Content_Type','Status_code','Status','Indexability_x','Indexability_status_x'
                            ,'X_robots_tag1','Meta_Robots_1_score','Meta_Refresh_1','Canonical_link_element1','rel_next_1','rel_prev_1','HTTP_rel_next_1','HTTP_rel_prev_1','amphtml_link_element',
                              'Readability','Link_score','Closest_Similarity_Match','NoNear_Duplicates','Spelling_Errors','Grammar_Errors','Hash','Last_modified','Redirect_URL',
                              'Redirect_type','Cookies','URL_Encoded_Address','Crawl_Timestamp','Type_1','Indexability_y','Indexability_Status_y', 'Date_added', 'Crawl_timestamp']

        # Supprimer les colonnes
        data_frame = data_frame.drop(columns=colonnes_exclues, errors='ignore')

        float_columns = ['Ttfb_babbar', 'Page_value_babbar', 'Page_trust_babbar', 'Semantic_value_babbar', 'Backlinks_babbar', 'Backlinks_host_babbar'
                         ,'Host_outlinks_babbar', 'Outlinks_babbar', 'Desktop_first_contentful_paint_terrain', 'Desktop_cumulative_layout_shift_terrain', 'Desktop_first_contentful_paint_lab',
                         'Desktop_largest_contentful_paint_lab','Desktop_speed_index_lab', 'SOSEO_yourtext_guru', 'DSEO_yourtext_guru', 'Word_count', 'Sentence_Count', 'Flesch_reading_ease_score', 'H1_2_length',
                         'Crawl_depth', 'Inlinks', 'Unique_inlinks', 'H2_2_score', 'H2_1_score', 'H1_1_score', 'Meta_Keywords1_score', 'Meta_Description1_score', 'Total_Types',
                         'Warnings', 'Unique_External_JS_Outlinks', 'Unique_External_Outlinks', 'External_Outlinks', 'Unique_Outlinks', 'of_Total', 'Desktop_cumulative_layout_shift_lab',
                         'Desktop_largest_contentful_paint_terrain', 'Desktop_first_input_delay_terain', 'Desktop_time_to_interactive_lab', 'Outlinks', 'Title1_pixel_width', 'Title2', 'Title2_length', 'H1_1_length', 'H2_2_length',
                         'Title2_pixel_width', 'Meta_description1', 'Meta_description1_Pixel_width', 'Meta_description2', 'Meta_description2_length', 'Meta_keywords1_length', 'H2_1_length',
                           'Meta_description2_Pixel_width', 'Meta_Keywords1', 'Meta_keywords_1','Meta_Keywords_1', 'H1_1','H1_2', 'H2_1', 'H2_2', 'Average_words_per_sentence', 'Response_time', 'Unique_JS_inlinks', 'Unique_JS_Outlinks', 'Errors', 
                           'Unique_Types', 'Meta_robots_1', 'Meta_robots_2', 'Meta_robots_3', 'Canonical_link_element2', 'Text_ratio', 'Meta_Description_1', 'Meta_description_1', 'URL_encoded_address', 'Title_1', 'Meta_Robots_1', 'Canonical_Link_Element_1', 'Canonical_link_element_1']
        
        existing_float_columns = [col for col in float_columns if col in data_frame.columns]

        # Appliquer la conversion uniquement sur les colonnes existantes
        data_frame[existing_float_columns] = data_frame[existing_float_columns].apply(pd.to_numeric, errors='coerce')
        data_frame[existing_float_columns].fillna(0, inplace=True)

        # Colonnes à convertir de string à float
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

        # Convertir le type des colonnes de string à float
        for colonne in columns_to_convert:
            if colonne in data_frame.columns:
                data_frame[colonne] = pd.to_numeric(data_frame[colonne], errors='coerce')
                data_frame[colonne].fillna(0, inplace=True)

        return data_frame

    def get_data_url_from_database(self):
        
        data_queryset = Data_Url.objects.values()
        df = pd.DataFrame.from_records(data_queryset)
        df = df.convert_dtypes()
        return df
    
    #Récupération de la data pour un url
    def get_data_for_1_urls(self,url,keyword,df,responseBuilder):

        self.url_data, testing   = self.get_data_for_url(url,keyword,df,responseBuilder)
        if isinstance(self.url_data, tuple) and len(self.url_data) > 0:
            # Extraire le premier élément, qui est un DataFrame
            extracted_df = self.url_data[0]

            # Vérifiez que c'est bien un DataFrame
            if isinstance(extracted_df, pd.DataFrame):
                self.url_data = extracted_df
            else:
                raise TypeError("Le premier élément du tuple n'est pas un DataFrame.")
        return self.url_data, testing    
            
    



    #Récupération de la data pour deux url
    def get_data_for_2_urls(self,url1,url2,keyword,df,responseBuilder):

        self.url_data   = self.get_data_for_url(url1,keyword,df,responseBuilder)
        self.url_data2  = self.get_data_for_url(url2,keyword,df,responseBuilder)



    #Récupération de la data pour un url
    def get_data_for_url(self,url,keyword,df,responseBuilder):

        df_key = df[df['Keyword'] == keyword]
        df_key_url = df_key[df_key['Url'] == url]
    
        if df_key_url.shape[0] > 0:
            testing= True
            return df_key_url.head(1), testing
        else:
            testing= False
            return self.get_url_data(url,keyword,responseBuilder), testing
        

       
    
       
    #Collecter la data d'une URL
    def get_url_data(self,url,keyword,responseBuilder):
        self.url        = url
        self.keyword    = keyword
        my_url_data = pd.DataFrame(data = {'Keyword': [keyword], 'Url': [url]})
        
        dc = DataColector()
        my_url_data = dc.get_all_URL_data(my_url_data)
        if responseBuilder.semantique_values_model == None :
            responseBuilder.semantique_values_model = SemantiqueValues()
        sm = responseBuilder.semantique_values_model
        my_url_data = sm.getSemantiqueValues(my_url_data)
        return my_url_data
        

  

     #Garder que les colonnes utiles pour la prédictions de la position de l'URL, pour un df de la classe   
    def fun_fun(self):
        
        print("Contenu du tuple:", self.url_data)
        print("Type de self.url_data:", type(self.url_data))
        print("Contenu de self.url_data:", self.url_data)
        

        if isinstance(self.url_data, tuple):
            # Assurez-vous qu'il contient un DataFrame ou des données qui peuvent être converties
            if len(self.url_data) > 0 and isinstance(self.url_data[0], pd.DataFrame):
                # Prenez le premier élément comme DataFrame
                self.url_data = self.url_data[0]
            else:
                raise TypeError("Le tuple ne contient pas de DataFrame.")
        
        test = self.url_data.copy()
        my_url_data=test[['Ttfb_babbar', 'Page_value_babbar', 'Page_trust_babbar',
                'Semantic_value_babbar', 'Backlinks_babbar', 'Backlinks_host_babbar',
                'Host_outlinks_babbar', 'Outlinks_babbar',
                'Desktop_first_contentful_paint_terrain',
                'Desktop_first_input_delay_terain',
                'Desktop_largest_contentful_paint_lab',
                'Desktop_cumulative_layout_shift_terrain',
                'Desktop_first_contentful_paint_lab', 'Desktop_speed_index_lab',
                'Desktop_largest_contentful_paint_lab',
                'Desktop_time_to_interactive_lab', 'Desktop_total_blocking_time_lab',
                'Desktop_cumulative_layout_shift_lab',
                'Unique_inlinks', 'Title1_pixel_width', 'Meta_description1_Pixel_width',
                'Mobile_first_contentful_paint_terrain',
                'Mobile_first_input_delay_terain',
                'Mobile_largest_contentful_paint_terrain',
                'Mobile_cumulative_layout_shift_terrain',
                'Mobile_first_contentful_paint_lab', 'Mobile_speed_index_lab',
                'Mobile_largest_contentful_paint_lab',
                'Mobile_time_to_interactive_lab', 'Mobile_total_blocking_time_lab',
                'Mobile_cumulative_layout_shift_lab',
                  'Score_1fr',
                'SOSEO_yourtext_guru', 'DSEO_yourtext_guru', 'Title1_length',
                'Meta_description1_length', 'H1_1_length', 'H2_1_length',
                'H2_2_length', 'Size_bytes', 'Word_count', 'Sentence_Count',
                'Inlinks', 'Outlinks', 'Unique_Outlinks', 'External_Outlinks',
                'Unique_External_Outlinks', 'Title1_score', 'Meta_Description1_score',
                'H1_1_score', 'H2_1_score', 'H2_2_score']]
        my_url_data = my_url_data.loc[:,~my_url_data.columns.duplicated()] 
        return my_url_data
    


    #Garder que les colonnes utiles pour la prédictions de la position de l'URL, pour n'importe quel df
    def fun_fun2(self,df):
        test = df.copy()
        my_url_data=test[['Ttfb_babbar', 'Page_value_babbar', 'Page_trust_babbar',
                'Semantic_value_babbar', 'Backlinks_babbar', 'Backlinks_host_babbar',
                'Host_outlinks_babbar', 'Outlinks_babbar',
                'Desktop_first_contentful_paint_terrain',
                'Desktop_first_input_delay_terain',
                'Desktop_largest_contentful_paint_lab',
                'Desktop_cumulative_layout_shift_terrain',
                'Desktop_first_contentful_paint_lab', 'Desktop_speed_index_lab',
                'Desktop_largest_contentful_paint_lab',
                'Desktop_time_to_interactive_lab', 'Desktop_total_blocking_time_lab',
                'Desktop_cumulative_layout_shift_lab',
                'Unique_inlinks', 'Title1_pixel_width', 'Meta_description1_Pixel_width',
                'Mobile_first_contentful_paint_terrain',
                'Mobile_first_input_delay_terain',
                'Mobile_largest_contentful_paint_terrain',
                'Mobile_cumulative_layout_shift_terrain',
                'Mobile_first_contentful_paint_lab', 'Mobile_speed_index_lab',
                'Mobile_largest_contentful_paint_lab',
                'Mobile_time_to_interactive_lab', 'Mobile_total_blocking_time_lab',
                'Mobile_cumulative_layout_shift_lab',
                  'Score_1fr',
                'SOSEO_yourtext_guru', 'DSEO_yourtext_guru', 'Title1_length',
                'Meta_description1_length', 'H1_1_length', 'H2_1_length',
                'H2_2_length', 'Size_bytes', 'Word_count', 'Sentence_Count',
                'Inlinks', 'Outlinks', 'Unique_Outlinks', 'External_Outlinks',
                'Unique_External_Outlinks', 'Title1_score', 'Meta_Description1_score',
                'H1_1_score', 'H2_1_score', 'H2_2_score']]
        return my_url_data
    

    #Cas de prédiction = 0
    def check_if_class1(self,model):
        
        if model.predict_proba(self.fun_fun())[0] == 0:
            return "Sorry i can 't help for this URL"
        return None
    
    #Remplacer la valeur par la median dans certaines colonnes
    def get_to_replace(self,df,y,col,actual):
        res = 0
        mean_X_top  = df[ y == 0 ][col].median()
        mean_X_flop = df[ y == 1 ][col].median()

        if mean_X_top > mean_X_flop:
            if mean_X_top > actual :
                #++
                res = mean_X_top + mean_X_top*0.1
            else:
                res = actual
        else:
            if mean_X_top < actual:
                #--
                res = mean_X_top - mean_X_top*0.1
            else:
                res = actual 
        return res
    

    def try_for_n_columns(self, model, df, y, n):
        res = ''
        TEST = False
        my_url_data = self.fun_fun().copy()
        columns = list(my_url_data.columns)
        column_combinations = combinations(columns, n)
        
        for col_comb in column_combinations:
            actual_values = [my_url_data.iloc[0][col] for col in col_comb]
            
            for col, actual in zip(col_comb, actual_values):
                my_url_data[col] = self.get_to_replace(df, y, col, actual)

            # Réorganiser les colonnes de self.url_data pour correspondre exactement à celles du modèle
            model_columns = model.get_booster().feature_names
            my_url_data = my_url_data.reindex(columns=model_columns).astype(np.float32)

            # Ajouter les colonnes manquantes à self.url_data avec des valeurs par défaut (zéro)
            for col in model_columns:
                if col not in my_url_data.columns:
                    my_url_data[col] = 0.0
                
            pred_res = model.predict_proba(my_url_data)[0][0]
            if pred_res > 0.5:
                res += f'for a proba of proba {pred_res} %\n'
                for col, actual in zip(col_comb, actual_values):
                    res += f'{col}\t      {float(actual)} -----> {float(my_url_data[col])}\n'
                res += 'OR...\n'
                TEST = True
        
        return TEST, res

    

    def try_for_columns(self, model, responseBuilder):
        print("*******************************************************Debut***************************************************************")
        find = False
        df = responseBuilder.df
        y = responseBuilder.trainedModels.y

        print("df", df)
        print("y", y)

        # S'assurer que df et y ont les mêmes index
        df = df.loc[y.index].copy()

        # Vérifier les dimensions après alignement
        print(f"df dimensions: {df.shape}")
        print(f"y dimensions: {y.shape}")
        print(self.url_data.dtypes)

        mean_x = df.median()
        self.url_data = self.url_data.fillna(mean_x)

        print(self.url_data)

        cols_to_remove = ['Keyword', 'Url', 'Top10']
        self.url_data = self.url_data.drop(columns=[col for col in cols_to_remove if col in self.url_data.columns], errors='ignore')

        # Récupérer les noms des colonnes du modèle
        model_columns = model.get_booster().feature_names

        # Réorganiser les colonnes de self.url_data pour correspondre exactement à celles du modèle
        self.url_data = self.url_data[model_columns].astype(np.float32)

        # Ajouter les colonnes manquantes à self.url_data avec des valeurs par défaut (zéro)
        missing_columns = set(model_columns) - set(self.url_data.columns)
        for col in missing_columns:
            self.url_data[col] = 0.0

        try:
            pred_res = model.predict_proba(self.url_data)[0][0]
            print("*******pred_res*****", pred_res)

            if pred_res > 0.5:
                res = f'you are on top with a probability of {pred_res}'
                find = True
            else:
                res = f'you are not on top with a probability of {pred_res}'
                find = False
            if find:
                print(res)
                return res, pred_res

            # Try for combinations of 1 to 5 columns
            for n in range(1, 6):
                find, res = self.try_for_n_columns(model, df, y, n)
                if find:
                    print(f"found for {n} columns")
                    return res, pred_res
                print(f'no for {n} col')

            return "sorry I didn't find any solution, good luck", pred_res
        except ValueError as e:
            print("Error during prediction:", e)
            return "An error occurred during prediction", None




    


    

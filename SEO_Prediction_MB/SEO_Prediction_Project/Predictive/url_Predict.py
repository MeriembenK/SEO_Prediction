from .SemantiqueValues import SemantiqueValues
from .data_colector import DataColector 
from SEO_Prediction_App.models import Data, Data_Url
import pandas as pd


class UrlPredect:

    #Constructeur de la classr UrlPredect
    def __init__(self) :
        self.url        = ''
        self.keyword    = ''
        self.url_data   = None
        self.url_data2  = None



    #Récupération de la data depuis la BDD
    def get_data_from_database(self):
        
        data_queryset = Data.objects.values()
        df = pd.DataFrame.from_records(data_queryset)
        df = df.convert_dtypes()
        return df
    
    def get_data_url_from_database(self):
        
        data_queryset = Data_Url.objects.values()
        df = pd.DataFrame.from_records(data_queryset)
        df = df.convert_dtypes()
        return df
    
    #Exclusion et conversion de certaines colonnes
    @staticmethod
    def exclude_and_convert_columns(data_frame):
        # Colonnes à exclure
        colonnes_exclues = ['id','Position', 'Url_Score', 'HTTP_Version', 'Http_code_babbar', 'Content_type',
                            'Status_code', 'Status', 'Indexability_x', 'Indexability_status_x', 'X_robots_tag1',
                            'Meta_Robots_1_score', 'Meta_Refresh_1', 'Canonical_link_element1', 'rel_next_1', 'rel_prev_1',
                            'HTTP_rel_next_1', 'HTTP_rel_prev_1', 'amphtml_link_element', 'Readability', 'Link_score',
                            'Closest_Similarity_Match', 'NoNear_Duplicates', 'Spelling_Errors', 'Grammar_Errors', 'Hash',
                            'Last_modified', 'Redirect_URL', 'Redirect_type', 'Cookies', 'URL_Encoded_Address', 'Crawl_Timestamp',
                            'Type_1', 'Indexability_y', 'Indexability_Status_y', 'Date_added']

        # Supprimer les colonnes
        data_frame = data_frame.drop(columns=colonnes_exclues, errors='ignore')

        # Colonnes à convertir de string à float
        colonnes_a_convertir = [ 'Ttfb_babbar', 'Page_value_babbar', 'Page_trust_babbar', 'Semantic_value_babbar', 'Backlinks_babbar', 'Backlinks_host_babbar'
                         , 'Host_outlinks_babbar', 'Outlinks_babbar', 'Desktop_first_contentful_paint_terrain', 'Desktop_cumulative_layout_shift_terrain', 'Desktop_first_contentful_paint_lab',
                         'Desktop_largest_contentful_paint_lab', 'SOSEO_yourtext_guru', 'DSEO_yourtext_guru', 'Word_count', 'Sentence_Count', 'Flesch_reading_ease_score', 'H1_2_length',
                         'Crawl_depth', 'Inlinks', 'Unique_inlinks', 'H2_2_score', 'H2_1_score', 'H1_1_score', 'Meta_Keywords1_score', 'Meta_Description1_score', 'Total_Types',
                         'Warnings', 'Unique_External_JS_Outlinks', 'Unique_External_Outlinks', 'External_Outlinks', 'Unique_Outlinks', 'of_Total', 'Desktop_cumulative_layout_shift_lab',
                         'Desktop_largest_contentful_paint_terrain', 'Desktop_first_input_delay_terain', 'Outlinks', 'Title1_pixel_width', 'Title2', 'Title2_length', 'H1_1_length', 'H2_2_length',
                         'Title2_pixel_width', 'Meta_description1', 'Meta_description1_Pixel_width', 'Meta_description2', 'Meta_description2_length', 'Meta_keywords1_length', 'H2_1_length',
                           'Meta_description2_Pixel_width', 'Meta_Keywords1', 'H1_1','H1_2', 'H2_1', 'H2_2', 'Average_words_per_sentence', 'Unique_JS_inlinks', 'Unique_JS_Outlinks', 'Errors', 
                           'Unique_Types', 'Meta_robots_1', 'Meta_robots_2', 'Meta_robots_3', 'Canonical_link_element2', 'Text_ratio', 'Response_time']

        # Convertir le type des colonnes de string à float
        data_frame[colonnes_a_convertir] = data_frame[colonnes_a_convertir].apply(pd.to_numeric, errors='coerce')
        data_frame[colonnes_a_convertir].fillna(0, inplace=True)


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
            data_frame[column] = pd.to_numeric(data_frame[column], errors='coerce', downcast='float')
            #print(data_frame.dtypes)
            if pd.api.types.is_categorical_dtype(data_frame[column]):
        # Gérer les colonnes catégoriques
             data_frame[column] = pd.to_numeric(data_frame[column], errors='coerce', downcast='float')

        return data_frame



    #Récupération de la data pour un url
    def get_data_for_1_urls(self,url,keyword,df,responseBuilder):
        self.url_data   = self.get_data_for_url(url,keyword,df,responseBuilder)



    #Récupération de la data pour deux url
    def get_data_for_2_urls(self,url1,url2,keyword,df,responseBuilder):

        self.url_data   = self.get_data_for_url(url1,keyword,df,responseBuilder)
        self.url_data2  = self.get_data_for_url(url2,keyword,df,responseBuilder)



    #Récupération de la data pour un url
    def get_data_for_url(self,url,keyword,df,responseBuilder):

        df_key = df[df['Thekeyword'] == keyword]
        df_key_url = df_key[df_key['Url'] == url]
    
        if df_key_url.shape[0] > 0:
            testing= True
            return df_key_url.head(1), testing
        else:
            testing= False
            return self.get_url_data(url,keyword,responseBuilder), testing
        


    #Collecter la data d'un URL
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
    


    #Remplacements et les prédictions colonne par colonne
    def try_for_1_column(self,model,df,y):
        res = ''
        TEST = False
        columns = list(self.fun_fun().columns)
        for col in columns:
            my_url_data = self.fun_fun()
            actual1 = my_url_data.iloc[0][col]
             
            my_url_data[col] = self.get_to_replace(df,y,col,actual1)

            pred_res = model.predict_proba(my_url_data)[0][0]
            if pred_res > 0.5 :
                    res = res + 'for a proba of proba ' +str(pred_res) + ' %' + '\n'
                    res = res + col +'\t      '+str(float(actual1))+' -----> '+ str(float(my_url_data[col])) + '\n'
                    res = res + 'OR...' + '\n'
                    TEST = True
        return TEST , res 
    

    
    #Remplacements et les prédictions par combinaison de colonnes 2 à 2
    def try_for_2_column(self,model,df,y):
        res = ''
        TEST = False
        columns = list(self.fun_fun().columns)
        for col1 in columns:
            columns2 = columns ; columns2.remove(col1)
            for col2 in columns2 :
                my_url_data = self.fun_fun()
                actual1 = my_url_data.iloc[0][col1]
                actual2 = my_url_data.iloc[0][col2]
                 
                my_url_data[col1] = self.get_to_replace(df,y,col1,actual1)
                my_url_data[col2] = self.get_to_replace(df,y,col2,actual2)
  
                pred_res = model.predict_proba(my_url_data)[0][0]
                if  pred_res > 0.5 :
                    res = res + 'for a proba of proba ' +str(pred_res) + ' %' + '\n'
                    res = res + col1 +'\t      '+str(float(actual1))+' -----> '+ str(float(my_url_data[col1])) + '\n'
                    res = res + col2 +'\t      '+str(float(actual2))+' -----> '+ str(float(my_url_data[col2])) + '\n'
                    res = res + 'OR...' + '\n'
                    TEST = True
        return TEST, res
    


    #Remplacements et les prédictions par combinaison de colonnes 3 à 3
    def try_for_3_column(self,model,df,y):   
        res = ''
        TEST = False
        columns = list(self.fun_fun().columns)     
        for col1 in columns:
            columns2 = columns; columns2.remove(col1)
            for col2 in columns2 :
                columns3 = columns2 ;columns3.remove(col2)
                for col3 in columns3 :
                    my_url_data = self.fun_fun()
                    actual1,actual2,actual3 = my_url_data.iloc[0][col1],my_url_data.iloc[0][col2], my_url_data.iloc[0][col3]

                    my_url_data[col1] = self.get_to_replace(df,y,col1,actual1)
                    my_url_data[col2] = self.get_to_replace(df,y,col2,actual2)
                    my_url_data[col3] = self.get_to_replace(df,y,col3,actual3)
 
                    pred_res = model.predict_proba(my_url_data)[0][0] 
                    if pred_res > 0.5 :
                        res = res + 'for a proba of proba ' +str(pred_res) + ' %' + '\n'
                        res = res + col1 +'\t      '+str(float(actual1))+' -----> '+ str(float(my_url_data[col1])) + '\n'
                        res = res + col2 +'\t      '+str(float(actual2))+' -----> '+ str(float(my_url_data[col2])) + '\n'
                        res = res + col3 +'\t      '+str(float(actual3))+' -----> '+ str(float(my_url_data[col3])) + '\n'
                        res = res + 'OR...' + '\n'
                        TEST = True
        return TEST , res
    

    
    #Remplacements et les prédictions par combinaison de colonnes 4 à 4
    def try_for_4_column(self,model,df,y):   
        res = ''
        TEST = False
        columns = list(self.fun_fun().columns)     
        for col1 in columns:
            columns2 = columns; columns2.remove(col1)
            for col2 in columns2 :
                columns3 = columns2 ;columns3.remove(col2)
                for col3 in columns3 :
                    columns4 = columns3 ;columns4.remove(col3)
                    for col4 in columns4 :
                        my_url_data = self.fun_fun()
                        actual1,actual2,actual3,actual4 = my_url_data.iloc[0][col1],my_url_data.iloc[0][col2], my_url_data.iloc[0][col3], my_url_data.iloc[0][col4]

                        my_url_data[col1] = self.get_to_replace(df,y,col1,actual1)
                        my_url_data[col2] = self.get_to_replace(df,y,col2,actual2)
                        my_url_data[col3] = self.get_to_replace(df,y,col3,actual3)
                        my_url_data[col4] = self.get_to_replace(df,y,col4,actual4)

                        pred_res = model.predict_proba(my_url_data)[0][0] 
                        if pred_res > 0.5 :
                            res = res + 'for a proba of proba ' +str(pred_res) + ' %' + '\n'
                            res = res + col1 +'\t      '+str(float(actual1))+' -----> '+ str(float(my_url_data[col1])) + '\n'
                            res = res + col2 +'\t      '+str(float(actual2))+' -----> '+ str(float(my_url_data[col2])) + '\n'
                            res = res + col3 +'\t      '+str(float(actual3))+' -----> '+ str(float(my_url_data[col3])) + '\n'
                            res = res + col4 +'\t      '+str(float(actual4))+' -----> '+ str(float(my_url_data[col4])) + '\n'
                            res = res + 'OR...' + '\n'
                            TEST = True
        return TEST , res
    


    #Remplacements et les prédictions par combinaison de colonnes 5 à 5
    def try_for_5_column(self,model,df,y):   
        res = ''
        TEST = False
        columns = list(self.fun_fun().columns)     
        for col1 in columns:
            columns2 = columns; columns2.remove(col1)
            for col2 in columns2 :
                columns3 = columns2 ;columns3.remove(col2)
                for col3 in columns3 :
                    columns4 = columns3 ;columns4.remove(col3)
                    for col4 in columns4 :
                        columns5 = columns4 ;columns5.remove(col4)
                        for col5 in columns5 :
                            my_url_data = self.fun_fun()
                            actual1,actual2,actual3,actual4,actual5 = my_url_data.iloc[0][col1],my_url_data.iloc[0][col2], my_url_data.iloc[0][col3], my_url_data.iloc[0][col4], my_url_data.iloc[0][col5]

                            my_url_data[col1] = self.get_to_replace(df,y,col1,actual1)
                            my_url_data[col2] = self.get_to_replace(df,y,col2,actual2)
                            my_url_data[col3] = self.get_to_replace(df,y,col3,actual3)
                            my_url_data[col4] = self.get_to_replace(df,y,col4,actual4)
                            my_url_data[col5] = self.get_to_replace(df,y,col5,actual5)

                            pred_res = model.predict_proba(my_url_data)[0][0] 
                            if pred_res > 0.5 :
                                res = res + 'for a proba of proba ' +str(pred_res) + ' %' + '\n'
                                res = res + col1 +'\t      '+str(float(actual1))+' -----> '+ str(float(my_url_data[col1])) + '\n'
                                res = res + col2 +'\t      '+str(float(actual2))+' -----> '+ str(float(my_url_data[col2])) + '\n'
                                res = res + col3 +'\t      '+str(float(actual3))+' -----> '+ str(float(my_url_data[col3])) + '\n'
                                res = res + col4 +'\t      '+str(float(actual4))+' -----> '+ str(float(my_url_data[col4])) + '\n'
                                res = res + col5 +'\t      '+str(float(actual5))+' -----> '+ str(float(my_url_data[col5])) + '\n'
                                res = res + 'OR...' + '\n'
                                TEST = True
        return TEST , res
    

    
    #Faire des prédictions en en essayant différente combinaisons de colonnes
    def try_for_columns(self,model,responseBuilder):
        find = False
        df = responseBuilder.df
        y  = responseBuilder.trainedModels.y
    
        mean_x = df.median()
        numeric_columns = self.url_data.select_dtypes(include='number').columns
        self.url_data[numeric_columns] = self.url_data[numeric_columns].fillna(0).astype(int)

        my_url_data = self.url_data
        
        print("Colonnes dans les données de test :", my_url_data.columns)

        pred_res = model.predict_proba(my_url_data)[0][0]
        print(pred_res)
        if  pred_res > 0.5 :
            print("pred_res est egale à",pred_res)
            res = 'you are on top yessss'
            find = True
            print(res)

        else :
            print("you are not on top")    
        res = ''
        find = True
        if find :
            print(res)
            return res
        find , res = self.try_for_1_column(model,df,y)
        if find :
            print(res)
            return res
        print('ùno for 1 col')
        find , res = self.try_for_2_column(model,df,y)
        if find :
            return res
        print('ùno for 2 col')
        find , res = self.try_for_3_column(model,df,y)
        if find :
            return res
        print('ùno for 3 col')
        find , res = self.try_for_4_column(model,df,y)
        if find :
            return res
        print('ùno for 4 col')
        find , res = self.try_for_5_column(model,df,y)
        if find :
            return res
        return "sorry i did't find any solution, good luck"
    
    

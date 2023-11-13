from SemantiqueValues import SemantiqueValues
from data_colector import DataColector 
import pandas as pd


class UrlPredect:
    def __init__(self) :
        self.url        = ''
        self.keyword    = ''
        self.url_data   = None
        self.url_data2  = None

    def get_data_for_1_urls(self,url,keyword,df,responseBuilder):
        self.url_data   = self.get_data_for_url(url,keyword,df,responseBuilder)

    def get_data_for_2_urls(self,url1,url2,keyword,df,responseBuilder):

        self.url_data   = self.get_data_for_url(url1,keyword,df,responseBuilder)
        self.url_data2  = self.get_data_for_url(url2,keyword,df,responseBuilder)


    def get_data_for_url(self,url,keyword,df,responseBuilder):
        df_key = df[df['Keyword'] == keyword]
        df_key_url = df_key[df_key['Url'] == url]
    
        if df_key_url.shape[0] > 0:
            return df_key_url.head(1)
        else:
            return self.get_url_data(url,keyword,responseBuilder)
        

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
        self.url_data.to_csv('check_data.csv')
        
    def fun_fun(self):
        test = self.url_data.copy()
        my_url_data=test[['TTFB (en ms) BABBAR', 'Page Value BABBAR', 'Page Trust BABBAR',
                'Semantic Value BABBAR', 'Backlinks BABBAR', 'Backlinks host BABBAR',
                'Host Outlinks BABBAR', 'Outlinks BABBAR',
                'Desktop First Contentful Paint Terrain',
                'Desktop First Input Delay Terain',
                'Desktop Largest Contentful Paint Terrain',
                'Desktop Cumulative Layout Shift Terrain',
                'Desktop First Contentful Paint Lab', 'Desktop Speed Index Lab',
                'Desktop Largest Contentful Paint Lab',
                'Desktop Time to Interactive Lab', 'Desktop Total Blocking Time Lab',
                'Desktop Cumulative Layout Shift Lab',
                'Unique Inlinks', 'Title 1 Pixel Width', 'Meta Description 1 Pixel Width',
                'Mobile First Contentful Paint Terrain',
                'Mobile First Input Delay Terain',
                'Mobile Largest Contentful Paint Terrain',
                'Mobile Cumulative Layout Shift Terrain',
                'Mobile First Contentful Paint Lab', 'Mobile Speed Index Lab',
                'Mobile Largest Contentful Paint Lab',
                'Mobile Time to Interactive Lab', 'Mobile Total Blocking Time Lab',
                'Mobile Cumulative Layout Shift Lab',
                  'Score_1fr',
                'SOSEO yourtext_guru', 'DSEO yourtext_guru', 'Title 1 Length',
                'Meta Description 1 Length', 'H1-1 Length', 'H2-1 Length',
                'H2-2 Length', 'Size (bytes)', 'Word Count', 'Sentence Count',
                'Inlinks', 'Outlinks', 'Unique Outlinks', 'External Outlinks',
                'Unique External Outlinks', 'Title 1 score', 'Meta Description 1 score',
                'H1-1 score', 'H2-1 score', 'H2-2 score']]#, 'Url score'
        return my_url_data
    
    def fun_fun2(self,df):
        test = df.copy()
        my_url_data=test[['TTFB (en ms) BABBAR', 'Page Value BABBAR', 'Page Trust BABBAR',
                'Semantic Value BABBAR', 'Backlinks BABBAR', 'Backlinks host BABBAR',
                'Host Outlinks BABBAR', 'Outlinks BABBAR',
                'Desktop First Contentful Paint Terrain',
                'Desktop First Input Delay Terain',
                'Desktop Largest Contentful Paint Terrain',
                'Desktop Cumulative Layout Shift Terrain',
                'Desktop First Contentful Paint Lab', 'Desktop Speed Index Lab',
                'Desktop Largest Contentful Paint Lab',
                'Desktop Time to Interactive Lab', 'Desktop Total Blocking Time Lab',
                'Desktop Cumulative Layout Shift Lab',
                'Unique Inlinks', 'Title 1 Pixel Width', 'Meta Description 1 Pixel Width',
                'Mobile First Contentful Paint Terrain',
                'Mobile First Input Delay Terain',
                'Mobile Largest Contentful Paint Terrain',
                'Mobile Cumulative Layout Shift Terrain',
                'Mobile First Contentful Paint Lab', 'Mobile Speed Index Lab',
                'Mobile Largest Contentful Paint Lab',
                'Mobile Time to Interactive Lab', 'Mobile Total Blocking Time Lab',
                'Mobile Cumulative Layout Shift Lab',
                  'Score_1fr',
                'SOSEO yourtext_guru', 'DSEO yourtext_guru', 'Title 1 Length',
                'Meta Description 1 Length', 'H1-1 Length', 'H2-1 Length',
                'H2-2 Length', 'Size (bytes)', 'Word Count', 'Sentence Count',
                'Inlinks', 'Outlinks', 'Unique Outlinks', 'External Outlinks',
                'Unique External Outlinks', 'Title 1 score', 'Meta Description 1 score',
                'H1-1 score', 'H2-1 score', 'H2-2 score']]#, 'Url score'
        return my_url_data
    
    def check_if_class1(self,model):
        
        if model.predict_proba(self.fun_fun())[0] == 0:
            return "Sorry i can 't help for this URL"
        return None
    
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
    #here i need to return the actual and sfdgrwfszxccv

    def try_for_columns(self,model,responseBuilder):
        find = False
        df = responseBuilder.df
        y  = responseBuilder.trainedModels.y
        mean_x = df.median()
        self.url_data = self.url_data.fillna(mean_x)
        my_url_data = self.url_data
        pred_res = model.predict_proba(my_url_data)[0][0]
        if  pred_res > 0.5 :
            res = 'you are on top'
            find = True
        res = 'you are on top'
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
    
    
           # self.trainedModels.models.get(values_for_pie[1][0])[0]
        

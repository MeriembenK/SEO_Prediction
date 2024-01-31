"""*********************************************************************PREDICTIONS RESPONSE***********************************************************************************"""
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
 
from operator import itemgetter 
import plotly.express as px
from Predictive.data_colector import DataColector 
from Predictive.train_Models import TrainModels
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
from Predictive.url_Predict import UrlPredect


class ResponseBuilder:

    def __init__(self) :

        self.semantique_values_model    = None 
        self.df                         = None 
        self.trainedModels              = None 
        self.sorted_model_result        = 'helllo there' 
        self.list_features              = []
        self.url_pred_res               = []
        self.info_of_data               = {}
        self.table_of_result            = None
        self.df_result_of_url_pred      = None
        self.url_pred_info              = None
        self.df_url                     = None
        self.p                          = 0
        self.nb_url                     = 100
        self.nb_top                     = 10
        self.keyword                    = ''
        self.keyword_url                = ''
        self.url_url                    = ''

    #def __init__(self,df,trainedModels,sorted_model_result) :
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    def get_info_data(self):
        x_init = self.df
        x_procesed = self.trainedModels.X
        y = self.trainedModels.y
        self.info_of_data = {"number of links":x_init['Url'].nunique(),"number of links Top":x_init[y == 0]['Url'].nunique(),"number of keywords":x_init['Keyword'].nunique(),"number of lines":x_procesed.shape[0],"number of columns":x_procesed.shape[1]} 
        print(self.info_of_data)

    def get_top(self,df,nb_top):
        df_r = df.copy()
        try:

            #df['Label_Top'] = df['Position'].apply(lambda x: "Top 10" if x <=10 else 'Pas Top 10')
            df_r['Top10'] = df_r['Position'].apply(lambda x: 0 if x <= nb_top else 1)
        except Exception:
            pass
        
        return df_r
    
    def drop_nb_url(self,df,nb_url):
        df_r = df.copy()
        return df_r[df_r['Position']<=nb_url]
    
    def train_model(self,df_input,nb_top,nb_url):
        df = df_input

        df = self.drop_nb_url(df,nb_url)
        
        self.df = self.get_top( df,nb_top)
        
        tm = TrainModels( )
        
        tm.train_models(self.df )
        self.trainedModels = tm
        self.get_info_data()
        

    def sort_models_result(self):
        models_res = self.trainedModels.models#['XGBClassifier']
        result_list = []
        for model in models_res:
                result = models_res.get(model)
                result_list.append([model,result[2]])

        result =result_list #sorted(result_list, key=itemgetter(1),reverse=True)
        print(result)
        return result
    

    def get_min_max(self):
        ##### get min - max of each feature
        #initial data
        x_init = self.df
        #x is the data aftre prepros
        x = self.trainedModels.X 
        #y is labels
        y = self.trainedModels.y 
        #get the collumns that i need from the init data
        x_init = x_init[list(x.columns)]
        #get the Top only from the init data ( top is the url that r on the first pos (in range 1-10))
        df1 = x_init[y == 0]
        #get the median of the top data 
        df2 = df1.median().to_frame().T
        #make a class here D want a class that have a range of 5 i know that it does'nt make sence but i dont have a choise
        df4 = pd.concat([df2-2,df2+3],ignore_index=True)
        #in case that the min is < 0 i put a 0
        df4 = df4.applymap(lambda x: x if x > 0 else 0 )
        #write on a format 
        df4 = df4.applymap('{:,.0f}'.format)
        #df4 = df4.applymap(str)
        df5 = (df4.iloc[0] +' - '+ df4.iloc[1]).to_frame().T

        return df5
    

    def get_table_of_result(self):
        print('hello hello hello : ')
        print(len(self.list_features))
        df = self.list_features[0].copy()
        df['score'] = (df[['score']]*100).applymap('{:,.2f}'.format)+' %'
        df['index'] = range(1, len(df) + 1) 
        col = df.pop("index")
        df.insert(0, col.name, col)  
        df = df.rename(columns={'min - max': 'min_max', 'what to do': 'WTD'}) 
        self.table_of_result = df

    
    def get_bar_plot(self , values, df5):
        fig = px.histogram(values , x="variable", y="score",color_discrete_sequence=['#0083F5'] 
            ).update_layout(xaxis_rangeslider_visible=True, xaxis_range=[-0.5, 10],plot_bgcolor="rgba(0, 0, 0, 0)" , paper_bgcolor= "rgba(0, 0, 0, 0)",font_color="white",
            ).update_traces(marker=dict(color= 'rgba(29,140,248,0.2)', line=dict(color='#1f8ef1', width=2))
            ).update_yaxes(showline=True, linewidth=1,linecolor='black', gridcolor='#4b4f75'
            ).update_xaxes(showline=False,)
        
        #     get data for the table of the model 1
        cols_names = list(values['variable'])
        data = {'features': cols_names, 'score': list(values['score']),'min - max': list(df5[[i for i in cols_names]].iloc[0])}
        df_data = pd.DataFrame(data)
        df_data = self.add_optimal_res(df_data)
        self.list_features.append( df_data)
        return fig
    

    def get_pie_plot(self,values_for_pie):
        fig = make_subplots(rows=1, cols=5,specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],subplot_titles=(values_for_pie[0][0], values_for_pie[1][0], values_for_pie[2][0], values_for_pie[3][0], values_for_pie[4][0]))
        fig .update_layout(  paper_bgcolor= "#27293D",font_color="white",  ) 
        
        val = float("{:.2f}".format(values_for_pie[0][1]*100))
        fig.add_trace(go.Pie(labels=['',''], values=[val,100-val],hole=0.8,textinfo='none',marker_colors=['#D048B6','rgb(240,240,240)'],),row=1, col=1),

        val2 = float("{:.2f}".format(values_for_pie[1][1]*100))
        fig.add_trace(go.Pie(labels=['',''],values=[val2,100-val2],hole=0.8,textinfo='none',marker_colors=['#D048B6','rgb(240,240,240)'], ),row=1, col=2),

        val3 = float("{:.2f}".format(values_for_pie[2][1]*100))   
        fig.add_trace(go.Pie(labels=['',''], values=[val3,100-val3],hole=0.8,textinfo='none',marker_colors=['#D048B6','rgb(240,240,240)'],),row=1, col=3),     
            
        val4 = float("{:.2f}".format(values_for_pie[3][1]*100))   
        fig.add_trace(go.Pie(labels=['',''], values=[val4,100-val4],hole=0.8,textinfo='none',marker_colors=['#D048B6','rgb(240,240,240)'],),row=1, col=4), 

        val5 = float("{:.2f}".format(values_for_pie[4][1]*100))   
        fig.add_trace(go.Pie(labels=['',''], values=[val5,100-val5],hole=0.8,textinfo='none',marker_colors=['#D048B6','rgb(240,240,240)'],),row=1, col=5), 

        fig.add_annotation(x=0.05, y=0.5,text=str(val)+"%",showarrow=False,font_size=23)
        fig.add_annotation(x=0.26, y=0.5,text=str(val2)+"%",showarrow=False,font_size=23)
        fig.add_annotation(x=0.5, y=0.5,text=str(val3)+"%",showarrow=False,font_size=23)
        fig.add_annotation(x=0.74, y=0.5,text=str(val4)+"%",showarrow=False,font_size=23)
        fig.add_annotation(x=0.95, y=0.5,text=str(val5)+"%",showarrow=False,font_size=23)
        fig.update_traces(showlegend=False)
        return fig


    def get_percentage_of_classes(self):
        y = self.df['Top10']
        nb_var = len(y)
        nb_not_top = sum(y)
        nb_top = len(y) - nb_not_top

        percentage_top = (100 * nb_top) / nb_var
        percentage_not_top = (100 * nb_not_top) / nb_var

        labels = ['Top', 'Not Top']
        values = [percentage_top, percentage_not_top]
        text = ["{0:.2f} %".format(i)  for i in values]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, text=text, textinfo='text', marker_colors=['#D048B6', 'rgb(240,240,240)'])]).update_layout(paper_bgcolor="#27293D", font_color="white", width=450, height=350, margin=dict(t=30))
    
        return fig, percentage_top, percentage_not_top



    def get_training_graphs(self):
        #getting the model
        models = self.trainedModels.models

        #sorting result
        values_for_pie = self.sort_models_result()

        #getting the min - max
        df5 = self.get_min_max()

        #### model 1 figure
        values = models.get(values_for_pie[0][0])
        #     bar plot for the model 1
        fig_BAR_1 = self.get_bar_plot(values[3],df5)
         

        #### model 2 fig
        values = models.get(values_for_pie[1][0]) 
        #     bar plot for the model 2
        fig_BAR_2 =self.get_bar_plot(values[3],df5)

        #### model 3 fig
        values = models.get(values_for_pie[2][0])
        #     bar plot for the model 3
        fig_BAR_3 = self.get_bar_plot(values[3],df5)

        print('end')
        print('start pie plot')
        # get the pie plot -- scores
        fig = self.get_pie_plot(values_for_pie)
        
        print('end') 
        fig_pourc = self.get_poucentage_of_classes()
        self.get_table_of_result()
        return fig.to_html(),fig_BAR_1.to_html(),   fig_BAR_2.to_html(),  fig_BAR_3.to_html()  ,fig_pourc.to_html() 
    

    def get_optimal_values(self, df_input):
        df =  self.df.copy()[list(df_input['features'])]
        y = self.df['Top10']
        
        res = {}
        for col  in list(df.columns):
            mean_X_top  = df[ y == 0 ][col].median()
            mean_X_flop = df[ y == 1 ][col].median()
            if mean_X_top > mean_X_flop:  
                #++ ✔️
                res[col] = '🟢' 
            else:
                #-- ❌
                res[col] = '🔴'
        return res
    
    def add_optimal_res(self,df):
        op_val = self.get_optimal_values(df)
        df = df.copy()
        result = []
        for col in list(df['features']):
            result.append(op_val.get(col))
        df['what to do'] = result
        return df


    def get_url_predect_result(self,url,keyword):
        # get the data
        print(url)
        print(keyword)

        df = self.df.copy()
        # get the data of the given url and keyword 
        up = UrlPredect() 
        up.get_data_for_1_urls(url,keyword,df,self)
        pos = up.url_data['Position'].iloc[0]

        # get the only features that i need from data
        up.url_data = up.fun_fun() 

        # get the result of traing model
        #values_for_pie = self.sort_models_result()
        # try to find what to change in ur url to bet on the top if u r not
        res = ""#up.try_for_columns(self.trainedModels.models.get(values_for_pie[1][0])[0],self) 
 
        res = res.split("\n")
        l = []
        for r in res :
            l.append( r )
        ### now i try to get the predectif table
        #get the data of the given url
        df = up.fun_fun2(df = up.url_data)
        
        # get the init df , x in the preproced data , y are the labels
        x_init = self.df
        x = self.trainedModels.X 
        y = self.trainedModels.y 

        # get the data of the top (labeled 0)
        df1 = x_init[y == 0]
        df1 = up.fun_fun2(df = df1)
        df2 = df1.median().to_frame().T
        #df2 = df2.applymap(lambda x: x if x > 1 else x*100 )
        df4 = pd.concat([df2-2,df2+3],ignore_index=True)
        df4 = df4.applymap(lambda x: x if x > 0 else 0 ) 

        df_ss = self.list_features[0].copy()
        what_to_do_list = list(df_ss['what to do'])
        features = list(df_ss['features'])
        df  = df [features]
        df4 = df4[features] 
        
        v1 = (df4.iloc[0] < df.iloc[0]).to_frame().T
        v2 = (df4.iloc[1] > df.iloc[0]).to_frame().T
        my_l = pd.DataFrame()
        cpt = 0
        for c in features: 
            if (v1[c].iloc[0] or what_to_do_list[cpt] == '🔴') and (v2[c].iloc[0] or what_to_do_list[cpt] == '🟢'): x = '✔️' 
            else: x = '❌'
            my_l[c] =  {1:x}
            cpt += 1
         
        df4 = pd.concat([df ,my_l ],ignore_index=True)
        l_of_features = list(df_ss['features'])
        df4 = df4[l_of_features].T
       
        df_ss['my_url'] = list(df4[0])
        df_ss['in range'] = list(df4[1])
        

        self.url_pred_res = [l,df_ss,l_of_features]
        self.get_url_predect_table()
        self.df_url = df  
        missing_val = df.isnull().sum().sum() 
        return [pos,missing_val]
  
    def get_url_predect_table(self):
        df = self.url_pred_res[1].copy()
        df['score'] = (df[['score']]*100).applymap('{:,.2f}'.format)+' %'
        df['index'] = range(1, len(df) + 1) 
        col = df.pop("index")
        df.insert(0, col.name, col)  
        self.df_result_of_url_pred =  df
         
    
    def get_list_for_form(self,df_url):
        list_result = []
        mini_list = []
        list_col = list(df_url.columns)
        cpt = 0
        for col in list_col:
            
            cpt += 1 
            val = df_url[col].iloc[0]
            mini_list.append((col,val))

            if cpt >= 4:
                cpt = 0
                list_result.append(mini_list)
                mini_list = []
        list_result.append(mini_list)
        return list_result
    

    def try_wbarith_request(self,df_url,request):

        values_for_pie = self.sort_models_result()
        model = self.trainedModels.models.get(values_for_pie[1][0])[0]

        for col in list(df_url):
            df_url[col] = float(request.GET.get(col))
   
        df_url = df_url[list(self.trainedModels.X.columns)]
        pred_res = model.predict_proba(df_url)[0][0]
        print('got the second part')
        if pred_res > 0.5:
            return True,df_url
        else:
            return False,df_url
        
    def check_keywords(self,key):
        dc = DataColector()
        keywords = dc.get_keywords(key)
        return keywords
    
    def add_keyword(self,key):
        with open("FIFO_keywords.txt", "a") as myfile:
            myfile.write(key+'\n')
        try:
            check = self.p.poll()
        except:
            check = 0
        if check is not None:
            c = subprocess.Popen(["python", "try_this.py"]) 
            self.p = c
        

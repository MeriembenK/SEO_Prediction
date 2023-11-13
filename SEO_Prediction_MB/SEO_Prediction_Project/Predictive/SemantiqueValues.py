
 
from sklearn.metrics.pairwise import cosine_similarity

from gensim.models import KeyedVectors
import nltk
try: 
    from nltk.corpus import stopwords
    from nltk import word_tokenize
except:
    nltk.download('stopwords')
    nltk.download('punkt')
    from nltk.corpus import stopwords
    from nltk import word_tokenize

import re 
import numpy as np
import pandas as pd


class SemantiqueValues:

    def __init__(self) :
        print('start')
        filename = 'C:/Users/mbennacer/Desktop/working D/plotly/the one/fasttextinstall/saved_as_word2vec.bin'
        
        self.ft =  KeyedVectors.load_word2vec_format(filename,binary=True)
        
        self.french_stopwords = list(set(stopwords.words('french')))
        #this function is to tokenise sentece and remove stopwords
        self.french_stopwords.append(',')
        self.french_stopwords.append(':')
        self.french_stopwords.append('dès')
        self.french_stopwords.append('ttc')
        print('done')
        
        
        self.filtre_stopfr =  lambda text: [token.lower() for token in text if (token.lower() not in self.french_stopwords) and ( not self.has_numbers(token)) ]

    def add_stopword(self,word):
        if word.lower() not in self.french_stopwords:
            self.french_stopwords.append(word.lower())
    
    def add_stopwords(self,words):
        for word in words:### normalenmnt je doit faire un split
            self.add_stopword(word)

    def get_stopwords(self):
        return self.french_stopwords

    def has_numbers(self,inputString):
            return bool(re.search(r'\d', inputString))

    def words_to_vectors(self,my_words):
        out_put = []
        for word in my_words:
            try:
                out_put.append(self.ft[word])
            except:
                pass
        return out_put
    
    def vectors_to_vector(self,sentence):
        vec = None
        for word in sentence:
            if vec is None:
                vec = word
            else:
                vec = np.add(vec,word)
        return np.divide(vec,len(sentence))
    
    def sentence_to_vector(self,sentence):
        words = self.filtre_stopfr( word_tokenize(sentence, language="french") )
        vectors = self.words_to_vectors(words)
        return self.vectors_to_vector(vectors)
    
    def my_function(self,str1,str2):
        str1 = str1.replace("-", " " )
        str2 = str2.replace("-", " " )
        str1 = str1.replace(",", " " )
        str2 = str2.replace(",", " " )
        str1 = str1.replace("(", " " )
        str2 = str2.replace("(", " " )
        str1 = str1.replace(")", " " )
        str2 = str2.replace(")", " " )
        try:
            if(str2 ==''): return 0
            return cosine_similarity([self.sentence_to_vector(str1)], [self.sentence_to_vector(str2)])[0][0] *100
        except:
            return 0
        
    def url_function(self,keyword,str1):
        str1 = re.sub(r'^https?:\/\/', '',str1)
        str1 = re.split(r'\W+',str1)
        ' '.join(str1)
        return self.my_function(keyword,' '.join(str1))
    
    def get_sementique_score(self,df):
        columns = ['Title 1','Meta Description 1','Meta Keywords 1','H1-1','H1-2','H2-1','H2-2','Meta Robots 1',]
        for column in columns:
            try:
                df[column] = df[column].fillna('')
                df[column + ' score'] =  df.apply(lambda x: self.my_function(x.Keyword,x[column]),axis=1 )
            except:
                pass
        column = 'Url'
        df[column] = df[column].fillna('')
        df[column + ' score'] =  df.apply(lambda x: self.url_function(x.Keyword,x[column]),axis=1 )
        return df

    def mini_fun(self,str1):
        if str(str1 == 'nan'):
            return '0'
        else:
            return str(str1).replace(',', '.')
        
    def data_to_numeric(self,df):
        columns = ['Average Words Per Sentence','Flesch Reading Ease Score','Text Ratio','% of Total','Response Time']
        for column in columns:
            try:
                df[column] =  df.apply( lambda x: self.mini_fun((x[column])),axis=1 )
                df[column] = pd.to_numeric(df[column])
            except:
                pass
        return df
    
    def data_to_drop(self,df):
        df = df.drop(columns=['Unnamed: 0','Unique Inlinks', 'HTTP Version','HTTP code BABBAR','Keyword','Url','Content Type','Status Code','Status','Indexability_x','Indexability Status_x','Title 1 Pixel Width','Meta Description 1 Pixel Width'])
        df = df.drop(columns=['X-Robots-Tag 1','Meta Robots 1 score','Meta Refresh 1','Canonical Link Element 1','rel="next" 1','rel="prev" 1','HTTP rel="next" 1','HTTP rel="prev" 1','amphtml Link Element','Readability','Link Score','Closest Similarity Match','No. Near Duplicates','Spelling Errors','Grammar Errors','Hash','Last Modified','Redirect URL','Redirect Type','Cookies','URL Encoded Address','Crawl Timestamp','Type-1','Indexability_y','Indexability Status_y'])
        df = df.drop(columns = list(df.columns[df.dtypes == 'object']))
                

        df = df.loc[:, df.isin([' ','NULL',0]).mean(axis=0) < .6]
        return df

    def getSemantiqueValues(self,df):
         
        df = self.get_sementique_score(df)
        df = self.data_to_numeric(df)
        #df = self.data_to_drop(df)
        return df




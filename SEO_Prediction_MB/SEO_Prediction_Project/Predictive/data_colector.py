"""**********************************************************************COLLECTION DES DONNEES************************************************************************************"""

from multiprocessing.pool import ThreadPool
from threading import Lock, Thread
from functools import partial
import subprocess
import threading
from fake_useragent import UserAgent
import pandas as pd
from selenium import webdriver
import urllib
import time
import random 
import requests
import numpy as np
import io
import re
import os
import logging
import requests
import itertools
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager
from .SemantiqueValues import SemantiqueValues
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin, urlparse 


class DataColector:
    #Création de la classe Datacloctor
    def __init__(self) :

        logging.basicConfig()
        self.data_lock      = Lock()
        self.threadLocal    = threading.local()
        self.used_proxy     = []
        self.cpt            = 0
        self.list_dfs       = [None,None,None,None,None]
        self.visited_urls = set()
        self.site_urls = set()
        



     #Avoir des mots clés similaires au mot clé sélectionné 
    def get_similar_keywords(self,keyword,nb_links):

        query = keyword
        query_norm = query.strip().replace('\s+',' ')
        query_norm = ' '.join(query_norm.split())
        query_norm = query_norm.replace(' ','+')                                
        api_keyword_url = f"https://api.semrush.com/?type=phrase_fullsearch&key=74a6648f76b3a2bceedc151079a0e2a3&phrase={query_norm}&export_columns=Ph&database=fr&display_limit={nb_links}&display_sort=nq_desc"
        response = requests.get(api_keyword_url)
        
        if response.status_code == 200:
            #Récupération et traitement des keyword retrournés
            keyword_data = response.text.replace('\r','')
            keyword_data = response.text.replace('\n','+')
            keyword_data = io.StringIO(keyword_data)
            keyword_df = pd.read_csv(keyword_data, sep="+")

            #Ajout de la requête dans les mots clés
            if query not in list(keyword_df['Keyword']):
                keyword_df = pd.concat([pd.DataFrame([{'Keyword':query}]), keyword_df], ignore_index=True)
            return list(keyword_df.get('Keyword'))
        else:
            return []
        



    #Récupération de l'URL grace au mot clé Semurush
    def find_URL_by_Keyword_SEMRUSH(self,keywords_list,nb_links):
        url_list = [] 

        #Pour chaque mot clé présent dans la liste, on récupère les premiers liens associés
        for keyword in keywords_list:

            #Formatage du mot clé pour l'API de Semrush
            keyword_norm = keyword.strip().replace('\s+',' ')
            keyword_norm = ' '.join(keyword_norm.split())
            keyword_norm = keyword_norm.replace(' ','+')

            #Préparation de la requête pour l'API de Semrush
            api_keyword_url = f"https://api.semrush.com/?type=phrase_organic&key=74a6648f76b3a2bceedc151079a0e2a3&phrase={keyword_norm}&export_columns=Ur&database=fr&display_limit={nb_links}&display_sort=nq_desc"
                            
            try:
                #Appel vers l'API de Semrush
                response = requests.get(api_keyword_url)

                #Récupération et traitement des keyword retrournés
                url_data = response.text.replace('\r','')
                url_data = response.text.replace('\n','*')
                url_data = io.StringIO(url_data)
                url_df = pd.read_csv(url_data, sep="*")
                
                #Ajout à la list des URLs
                url_df.get('Url')
                url_list += [(keyword, position+1, url) for position, url in enumerate(list(url_df.get('Url')))]

            except:
                #En cas d'erreur
                print(f"No reponse for {keyword}") 
    
        #Création d'un DataFrame à partir de la liste précédemment obtenue
        df = pd.DataFrame(url_list, columns = ['Keyword', 'Position', 'Url'])

        # Sort the DataFrame by keyword and position.
        df = df.sort_values(by = ['Keyword', 'Position'], ignore_index=True)
        
        return df
    



    #Définir si c'est top ou pas
    def get_top(self,df,nb_top):
        
        try:
            df['Top10'] = df['Position'].apply(lambda x: 0 if x <= nb_top else 1)
        except Exception:
            pass
        
        return df



    def crawl_url(self, url, depth, max_depth):
        if depth > max_depth or url in self.visited_urls:
            return

        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

            # Ajoutez les liens absolus au jeu des URLs du site
            self.site_urls.update(links)

            # Ajoutez cette URL à l'ensemble des URLs visités
            self.visited_urls.add(url)

            # Explorez récursivement les liens internes du site
            for link in links:
                absolute_link = urljoin(url, link)
                if urlparse(absolute_link).netloc == urlparse(url).netloc:
                    self.crawl_url(absolute_link, depth + 1, max_depth)

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des liens pour le site {url}: {e}")


    def get_all_site_urls(self, start_url, max_depth=3):
        self.crawl_url(start_url, 0, max_depth)
        return list(self.site_urls)



    def multiprocessing_function(self,nb,df, function, pool=10, target=['Url'], join=['Url'], how='left', name=''):
        
        self.cpt = 0
        #Liste unique de la colonne cible
        print('hello')
        if len(target)>1:
            unique_list_1 = list(set(df.get(target[0])))
            unique_list = [(x,list(df[df['Keyword']==x].get(target[1]))) for x in unique_list_1]
        
        else:
            unique_list = list(set(df.get(target[0])))
        # Liste partagée entre les Threads
        dfs_list = []
        
        # ------ Multiprocessing pour crawler toutes les Urls -------
        ThreadPool(pool).map(partial(function, df=dfs_list, list_len=len(unique_list), pool=pool), unique_list)
        #Conversion de la liste partagée en un Data Frame
        df_function = pd.DataFrame.from_dict(list(dfs_list), orient='columns')
        
        # ------ Fusion avec le DataFrame d'origine ------
        df = pd.merge(df, df_function, how=how, left_on = join, right_on = join) 
        
        self.list_dfs.insert(nb,df)

        return df
     


    def get_driver(self,):
        pro = []
        
        driver = getattr(self.threadLocal, 'driver', None)
        if driver is None:
            options = webdriver.FirefoxOptions()
            options.add_argument("--lang=fr")

            
            #Si tous les proxy sont utilisés, on en prend un aléatoirement pour l'utiliser ou on utilise l'adresse IP de la machine de l'utilisateur
            if self.used_proxy == len(pro) and self.used_proxy > 0:
                
                index = random.randint(0,len(pro))
                if index == len(pro):
                    #On initialise pas de proxy (donc on utilise la machine l'IP de la machine courante pour faire les calculs)
                    pass
                else:
                    #On utilise un proxy
                    PROXY = f"{proxy[index]}:{proxy[index]}"
                    options.add_argument('--proxy-server=%s' % PROXY)
            else: 
                
                #On prend un proxy qui n'est pas utilisé
                not_used_proxy_list = list(set(pro) - set(self.used_proxy))
                if not_used_proxy_list:
                    proxy = not_used_proxy_list[0]
                    self.used_proxy.append(proxy)
                    PROXY = f"{proxy[0]}:{proxy[1]}"
                    options.add_argument('--proxy-server=%s' % PROXY)
            
            options.add_argument("--log-level=3")
            
            options.page_load_strategy = 'normal'
            
            ua = UserAgent(verify_ssl=False)
            
            userAgent = ua.random
            
            print(userAgent)
            
            options.add_argument(f'user-agent={userAgent}')
            #options.add_experimental_option('excludeSwitches', ['enable-logging'])

             
            
            options.add_argument("--headless")  # Run in headless mode
            options.add_argument("--disable-gpu")  # Disable GPU acceleration

            # Create a WebDriver instance using Chromium WebDriver and options
            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install() ,options= options)
            setattr(self.threadLocal, 'driver', driver)
             
        return driver




    def get_babbarTech_scores(self,url, df, list_len, pool):
        API_KEY = "lrU6gM7ev17v45DTS45dqznlEVvoapsNIotq5aQMeusGOtemdrWlqcpkIIMv"
        API_URL = 'https://www.babbar.tech/api/url/overview/main'
        
        self.cpt += 1

        start_thread = time.time()

        BABBARTECH = True
        
        #Variable pour s'assurer qu'on est bien connecté
        CONNEXION_BABBARTECH = True
        
            # ---------------- Récupération des informations de BabbarTech ------------------------
            #Si on est connecté
        if CONNEXION_BABBARTECH:

                #On crée un URL afin de se rendre directement sur la page avec les infos de l'URL
                #Cela évite de passer par des clicks, entrée des URLs, changement de Host en URL...
                time.sleep(3)
                res = requests.post(API_URL + '?api_token=' + API_KEY,
                                json = {'url' : url})
                
                if BABBARTECH:
                    time.sleep(random.uniform(0.5,1.25))
                    
                    try:
                        http_code = float(res.json()['httpStatus'])
                    except Exception:
                        http_code = np.nan
                    #Récupération des informations
                    try:                               
                        ttfb = float(res.json()['fetchTimeToFirstByte'])
                    except Exception:
                        ttfb = np.nan
                    try:
                        page_value = float(res.json()['pageValue'])
                    except Exception:
                        page_value = np.nan
                    try:
                        page_trust = float(res.json()['pageTrust'])
                    except Exception:
                        page_trust = np.nan                                  
                    try:                                                
                        semantic_value = float(res.json()['semanticValue'])
                    
                    except Exception:
                        semantic_value = np.nan
                    try:
                        backlinks = float(res.json()['backlinksExternal'])## what backlinks
                    except Exception:
                        backlinks = np.nan
                    try:                                                   
                        host_backlinks = float(res.json()['backlinksInternal'])
                    except Exception:
                        host_backlinks = np.nan
                    try:
                        host_outlinks = float(res.json()['numOutLinksInt'])
                    except Exception:
                        host_outlinks = np.nan  
                    
                    try:                                                   
                        outlinks = float(res.json()['numOutLinksExt'])
                    except Exception:
                        outlinks = np.nan
                        #Insertion des informations dans la liste
                    with self.data_lock:
                        df.append({'Url' : url, 'HTTP code BABBAR':http_code, 'TTFB (en ms) BABBAR' : ttfb, 'Page Value BABBAR' : page_value , 'Page Trust BABBAR' : page_trust ,
                        'Semantic Value BABBAR' : semantic_value, 'Backlinks BABBAR' : backlinks, 'Backlinks host BABBAR' : host_backlinks, 'Host Outlinks BABBAR' : host_outlinks, 'Outlinks BABBAR' : outlinks})
                    #print("J'affiche1",df)       
        now_thread = time.time()





    def get_pageSpeed_scores_API(self,url, df, list_len, pool):

        #Appel de la requête pour avoir les mots clés
        
        self.cpt += 1

        start_thread = time.time()

        url_norm = urllib.parse.quote_plus(url)
        
        response = requests.get(f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy=desktop&url={url_norm}")
    
        nb_req_max = 2
        nb_req = 0
        # Trop de requête par minute, on relance la requête au bout de 65 secondes
        while response.status_code == 429 and nb_req < nb_req_max:
            nb_req += 1
            time.sleep(25)
            response = requests.get(f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy=desktop&url={url_norm}")

        # Tout s'est bien passé
        if response.status_code == 200:
            #Terrain
            try:
                fcp_terrain = float(response.json().get('loadingExperience', np.nan).get('metrics', np.nan).get('FIRST_CONTENTFUL_PAINT_MS', np.nan).get('percentile', np.nan))
            except Exception:
                fcp_terrain = np.nan
            try:
                fid_terrain = float(response.json().get('loadingExperience', np.nan).get('metrics', np.nan).get('FIRST_INPUT_DELAY_MS', np.nan).get('percentile', np.nan))
            except Exception:
                fid_terrain = np.nan
            try:
                lcp_terrain = float(response.json().get('loadingExperience', np.nan).get('metrics', np.nan).get('LARGEST_CONTENTFUL_PAINT_MS', np.nan).get('percentile', np.nan))
            except Exception:
                lcp_terrain = np.nan
            try:
                cls_terrain = float(response.json().get('loadingExperience', np.nan).get('metrics', np.nan).get('CUMULATIVE_LAYOUT_SHIFT_SCORE', np.nan).get('percentile', np.nan))
            except Exception:
                cls_terrain = np.nan
            #Laboratoire
            try:
                fcp_lab = float(response.json().get('originLoadingExperience', np.nan).get('metrics', np.nan).get('FIRST_CONTENTFUL_PAINT_MS', np.nan).get('percentile', np.nan))
            except Exception:
                fcp_lab = np.nan
            try:
                lcp_lab = float(response.json().get('originLoadingExperience', np.nan).get('metrics', np.nan).get('LARGEST_CONTENTFUL_PAINT_MS', np.nan).get('percentile', np.nan))
            except Exception:
                lcp_lab = np.nan
            try:
                cls_lab = float(response.json().get('originLoadingExperience', np.nan).get('metrics', np.nan).get('CUMULATIVE_LAYOUT_SHIFT_SCORE', np.nan).get('percentile', np.nan))
            except Exception:
                cls_lab = np.nan
            try:
                speed_index_lab = float(response.json().get('lighthouseResult', np.nan).get('audits', np.nan).get('speed-index', np.nan).get('numericValue', np.nan))
            except Exception:
                speed_index_lab = np.nan
            try:
                time_interative_lab = float(response.json().get('lighthouseResult', np.nan).get('audits', np.nan).get('interactive', np.nan).get('numericValue', np.nan))
            except Exception:
                time_interative_lab = np.nan
            try:
                total_bloc_time = float(response.json().get('lighthouseResult', np.nan).get('audits', np.nan).get('total-blocking-time', np.nan).get('numericValue', np.nan))
            except Exception:
                total_bloc_time = np.nan

            #Ajout dans la liste résultante des informations extraites
            with self.data_lock:
                df.append({'Url' : url, 
                        #Données terrain
                        'Desktop First Contentful Paint Terrain' : fcp_terrain, 'Desktop First Input Delay Terain' : fid_terrain, 'Desktop Largest Contentful Paint Terrain' : lcp_terrain, 'Desktop Cumulative Layout Shift Terrain' : cls_terrain,
                        #Données laboratoire
                        'Desktop First Contentful Paint Lab' : fcp_lab, 'Desktop Speed Index Lab' : speed_index_lab, 'Desktop Largest Contentful Paint Lab' :  lcp_lab, 'Desktop Time to Interactive Lab' : time_interative_lab,'Desktop Total Blocking Time Lab' :  total_bloc_time, 'Desktop Cumulative Layout Shift Lab' : cls_lab
                })
                            
        else:
            #Ajout dans la liste résultante des informations extraites
            with self.data_lock:
                df.append({'Url' : url, 
                        #Données terrain
                        'Desktop First Contentful Paint Terrain' : np.nan, 'Desktop First Input Delay Terain' : np.nan, 'Desktop Largest Contentful Paint Terrain' : np.nan, 'Desktop Cumulative Layout Shift Terrain' : np.nan,
                        #Données laboratoire
                        'Desktop First Contentful Paint Lab' : np.nan, 'Desktop Speed Index Lab' : np.nan, 'Desktop Largest Contentful Paint Lab' :  np.nan, 'Desktop Time to Interactive Lab' : np.nan,'Desktop Total Blocking Time Lab' :  np.nan, 'Desktop Cumulative Layout Shift Lab' : np.nan
                })
        #print("J'affiche2",df)
        now_thread = time.time()




    def get_pageSpeed_mobile_scores_API(self,url, df, list_len, pool):

        #Appel de la requête pour avoir les mots clés
        
        self.cpt += 1

        start_thread = time.time()

        url_norm = urllib.parse.quote_plus(url)
        
        response = requests.get(f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy=mobile&url={url_norm}")

        nb_req_max = 2
        nb_req = 0
        # Trop de requête par minute, on relance la requête au bout de 65 secondes
    
        while response.status_code == 429 and nb_req < nb_req_max:
            nb_req += 1
            time.sleep(25)
            response = requests.get(f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy=mobile&url={url_norm}")

        # Tout s'est bien passé
        if response.status_code == 200:
            #Terrain
            try:
                fcp_terrain = float(response.json().get('loadingExperience', np.nan).get('metrics', np.nan).get('FIRST_CONTENTFUL_PAINT_MS', np.nan).get('percentile', np.nan))
            except Exception:
                fcp_terrain = np.nan
            try:
                fid_terrain = float(response.json().get('loadingExperience', np.nan).get('metrics', np.nan).get('FIRST_INPUT_DELAY_MS', np.nan).get('percentile', np.nan))
            except Exception:
                fid_terrain = np.nan
            try:
                lcp_terrain = float(response.json().get('loadingExperience', np.nan).get('metrics', np.nan).get('LARGEST_CONTENTFUL_PAINT_MS', np.nan).get('percentile', np.nan))
            except Exception:
                lcp_terrain = np.nan
            try:
                cls_terrain = float(response.json().get('loadingExperience', np.nan).get('metrics', np.nan).get('CUMULATIVE_LAYOUT_SHIFT_SCORE', np.nan).get('percentile', np.nan))
            except Exception:
                cls_terrain = np.nan
            #Laboratoire
            try:
                fcp_lab = float(response.json().get('originLoadingExperience', np.nan).get('metrics', np.nan).get('FIRST_CONTENTFUL_PAINT_MS', np.nan).get('percentile', np.nan))
            except Exception:
                fcp_lab = np.nan
            try:
                lcp_lab = float(response.json().get('originLoadingExperience', np.nan).get('metrics', np.nan).get('LARGEST_CONTENTFUL_PAINT_MS', np.nan).get('percentile', np.nan))
            except Exception:
                lcp_lab = np.nan
            try:
                cls_lab = float(response.json().get('originLoadingExperience', np.nan).get('metrics', np.nan).get('CUMULATIVE_LAYOUT_SHIFT_SCORE', np.nan).get('percentile', np.nan))
            except Exception:
                cls_lab = np.nan
            try:
                speed_index_lab = float(response.json().get('lighthouseResult', np.nan).get('audits', np.nan).get('speed-index', np.nan).get('numericValue', np.nan))
            except Exception:
                speed_index_lab = np.nan
            try:
                time_interative_lab = float(response.json().get('lighthouseResult', np.nan).get('audits', np.nan).get('interactive', np.nan).get('numericValue', np.nan))
            except Exception:
                time_interative_lab = np.nan
            try:
                total_bloc_time = float(response.json().get('lighthouseResult', np.nan).get('audits', np.nan).get('total-blocking-time', np.nan).get('numericValue', np.nan))
            except Exception:
                total_bloc_time = np.nan

            #Ajout dans la liste résultante des informations extraites
            with self.data_lock:
                df.append({'Url' : url, 
                        #Données terrain
                        'Mobile First Contentful Paint Terrain' : fcp_terrain, 'Mobile First Input Delay Terain' : fid_terrain, 'Mobile Largest Contentful Paint Terrain' : lcp_terrain, 'Mobile Cumulative Layout Shift Terrain' : cls_terrain,
                        #Données laboratoire
                        'Mobile First Contentful Paint Lab' : fcp_lab, 'Mobile Speed Index Lab' : speed_index_lab, 'Mobile Largest Contentful Paint Lab' :  lcp_lab, 'Mobile Time to Interactive Lab' : time_interative_lab,'Mobile Total Blocking Time Lab' :  total_bloc_time, 'Mobile Cumulative Layout Shift Lab' : cls_lab
                })
                            
        else:
            #Ajout dans la liste résultante des informations extraites
            with self.data_lock:
                df.append({'Url' : url, 
                        #Données terrain
                        'Mobile First Contentful Paint Terrain' : np.nan, 'Mobile First Input Delay Terain' : np.nan, 'Mobile Largest Contentful Paint Terrain' : np.nan, 'Mobile Cumulative Layout Shift Terrain' : np.nan,
                        #Données laboratoire
                        'Mobile First Contentful Paint Lab' : np.nan, 'Mobile Speed Index Lab' : np.nan, 'Mobile Largest Contentful Paint Lab' :  np.nan, 'Mobile Time to Interactive Lab' : np.nan,'Mobile Total Blocking Time Lab' :  np.nan, 'Mobile Cumulative Layout Shift Lab' : np.nan
                })
        #print("j'affiche3", df)
        now_thread = time.time()





    def get_1fr_scores(self,url, df, list_len, pool):
        self.cpt += 1
        start_thread = time.time()
        UNFR = True

        #On place le Driver sur l'Url
        driver = self.get_driver()
        try:
            driver.get("https://1.fr/signin")
        except Exception:
            print(f"Impossible de se connecter à {url}")
            UNFR = False
        
        if UNFR:
            try:
                #Mail
                """mail_input_ahref = driver.find_element("xpath", "/html/body/div[2]/div/div[2]/div/div/div[1]/form/input[4]")
                mail_input_ahref.send_keys('tools@eskimoz.fr')

                #Mot de passe
                pwd_input_ahref = driver.find_element("xpath", "/html/body/div[2]/div/div[2]/div/div/div[1]/form/input[5]")
                pwd_input_ahref.send_keys('o|N(>)ce&633')

                #Bouton de connexion
                login_button_ahref = driver.find_element("xpath", "/html/body/div[2]/div/div[2]/div/div/div[1]/form/div[4]/input")
                login_button_ahref.submit() 
                
                time.sleep(random.uniform(0.5,1.25))"""
            
            except Exception:
                print('Déjà connecté')  
            while True:
                driver.get("https://1.fr/")
                time.sleep(random.uniform(1.5,2.25))
                #On tape l'URL//*[@id="url"]            
                url_input = driver.find_element("xpath", "/html/body/div[2]/div[1]/div[2]/div/div/div/div[1]/form/table/tbody/tr/td[1]/input")
                url_input.clear()

                for char in url:
                    url_input.send_keys(char)
                    time.sleep(random.uniform(0.01,0.15))

                #On appuie sur le bouton GO
                search_input = driver.find_element("xpath", "/html/body/div[2]/div[1]/div[2]/div/div/div/div[1]/form/table/tbody/tr/td[2]/input")
                search_input.submit()
                time.sleep(random.uniform(1.5,2.25))
                #Si on lance trop de requetes à la fois, on doit patienter
                try:
                    error_div = driver.find_element("xpath", "//*[contains(text(), 'trop de requêtes en provenance de votre IP')]")
                    time.sleep(random.uniform(1,2)) 
                except Exception:
                    #S'il n'y a pas d'erreur, on sort de la boucle
                    break

            #Acceptation des cookies
            try:
                cookies_button = driver.find_element_by_id("cookiescript_accept").click()
            except Exception:
                time.sleep(random.uniform(0.5,1.2))

            #Récupération du score
            try:
                #Cas classique (seulement un pourcentage0
                score_1fr = driver.find_element("xpath", "/html/body/div[3]/div[2]/table/tbody/tr/td/span")
                print(score_1fr)
                score_1fr = float(re.sub('Score: ([0-9]+(.[0-9]+)?)%','\g<1>', score_1fr.text))
                print(score_1fr)
                with self.data_lock:
                    df.append({'Url' : url, 'Score_1fr' : score_1fr})
            except Exception:
                try:       
                    #Cas 'Je ne suis pas sûr de bien comprendre votre texte (XX%).Ajoutez plus de texte et réessayez.'    
                    #                                         /html/body/div[3]/div[2]/table/tbody/tr/td/span                     
                    score_1fr = driver.find_element("xpath", "/html/body/div[3]/div[2]/div[1]/table/tbody/tr/td[1]/p")
                    score_1fr = float(re.sub('[^0-9]*([0-9]+(.[0-9]+)?)%[^0-9]*','\g<1>', score_1fr.text))
                    with self.data_lock:
                        df.append({'Url' : url, 'Score_1fr' : score_1fr})
                except:
                    #Autre cas (erreur)
                    with self.data_lock:
                        df.append({'Url' : url, 'Score_1fr' : np.nan})
        else:
            with self.data_lock:
                df.append({'Url' : url, 'Score_1fr' : np.nan})
        #print("J'affiche4",df) 
        #app.update_progressBar('1.Fr', list_len, floor(now_thread - start_thread)/pool)
    



    def get_yourTextGuru_scores(self,keyword, df, list_len, pool):
        start_thread = time.time()

        #Variable pour s'assurer que la création du guide est terminé
        GUIDE_DONE = True 
        YOURTEXTGURU = True

        # ------ Connexion ------
        #On place le driver sur l'URL Ahref
        driver = self.get_driver()
        
        try:
            driver.get("https://yourtext.guru/order-premium")
            #https://1.fr/signin
        except Exception:
            print(f"Impossible de se connecter à {keyword}")
            YOURTEXTGURU = False
        
        if YOURTEXTGURU:
            try:
                #Mail
                mail_input_ahref = driver.find_element("xpath", "/html/body/div/div[2]/section/div/div[2]/div/div/div/form/p[1]/input")
                mail_input_ahref.send_keys('dahernandez@karavel.com')

                #Mot de passe
                pwd_input_ahref = driver.find_element("xpath", "/html/body/div/div[2]/section/div/div[2]/div/div/div/form/p[2]/input")
                pwd_input_ahref.send_keys('@Karavel@2022@')

                #Bouton de connexion
                login_button_ahref = driver.find_element("xpath", "/html/body/div/div[2]/section/div/div[2]/div/div/div/form/p[4]/input")
                login_button_ahref.submit()
                
                time.sleep(random.uniform(0.5,1.25))
            except Exception:
                print('Déjà connecté')  
            
            # ------ Création des guides par mot clé ------
            
            #On place dle driver sur la création de guide
            while True:
                driver.get("https://yourtext.guru/order-premium")

                try:
                    #Insertion du mot clé                      
                    keyword_input = driver.find_element("xpath", "/html/body/div[2]/div/div[2]/div/div/div/div/div[2]/form/div[2]/div/div[1]/textarea")
                    keyword_input.send_keys(keyword[0])

                    #Modification du groupe en Predictive
                    group_input = driver.find_element("xpath", "/html/body/div[2]/div/div[2]/div/div/div/div/div[2]/form/div[6]/div/div/input")
                    group_input.send_keys("Predictive")

                    #Génération du guide
                    guide_button = driver.find_element("xpath", "/html/body/div[2]/div/div[2]/div/div/div/div/div[2]/form/div[8]/div/button")
                    guide_button.submit()

                    time.sleep(random.uniform(2, 4))

                    #On récupère la clé du guide   
                    while True:  
                        try:        
                            guide_key = driver.find_element("xpath", "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[2]").text
                            break
                        except :
                            time.sleep(random.uniform(2, 4))    

                    print('helllo 1')
                    #On attend que le guide se crée 
                    start = now = time.time()
                    while True:
                        try:                                 
                        
                            if driver.find_element("xpath", '/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[7]').text == '100%' or (now - start > 300):
                                break   
                            time.sleep(2)                     
                        except Exception:
                            GUIDE_DONE = False
                            break
                        now = time.time()
                    
                except Exception:
                    GUIDE_DONE = False
                try:
                    driver.get(f'https://yourtext.guru/stats/{guide_key}')
                    time.sleep(random.uniform(1, 2.5))
                    if driver.find_element("xpath", '/html/body/div/div/div/div[1]').text != '403':
                        break
                except:
                    break
            # ------ Récupération des informations du guide ------
            
            if GUIDE_DONE:
                
                try:
                    #On se rend sur le guide
                    #time.sleep(random.uniform(1, 2.5))
                    #driver.get(f'https://yourtext.guru/stats/{guide_key}')
                    time.sleep(random.uniform(1, 2.5))
                    
                    
                    for i in range(len(keyword[1])):
                        j = 0
                        url_found = False
                        #Url 
                        # get how much url wehave per default   
                        nb = 0
                        try:
                            a = 1   
                            while True:    
                                                    
                                url = driver.find_element("xpath", f"/html/body/div[2]/div/div[2]/div/div[12]/div/div/div[2]/table/tbody/tr[{a}]/td[2]").text
                                url = url.split('\n')[0]
                                nb += 1
                                if url == keyword[1][i]:
                                    url_found = True
                                    
                                    break
                                a += 1
                                
                        except:
                            pass
                        
                        try:      
                            if not url_found:
                                time.sleep(3)                      
                                pwd_input_ahref = driver.find_element("xpath", f"/html/body/div[2]/div/div[2]/div/div[12]/div/div/div[2]/table/tbody/tr[{nb}]/td[2]/input")
                                pwd_input_ahref.send_keys(keyword[1][i])
                                url = keyword[1][i]
                                #Bouton de connexion                                
                                login_button_ahref = driver.find_element("xpath", f"/html/body/div[2]/div/div[2]/div/div[12]/div/div/div[2]/table/tbody/tr[{nb}]/td[2]/button")
                                login_button_ahref.click()
                            

                            #Soseo                     
                            try:
                                
                                if url_found :
                                    raise Exception()
                                
                                time.sleep(5)
                                alert = driver.switch_to.alert
                                text = alert.text
                                alert.accept()
                                j-=1
                                if text == 'Vous avez dépassé la limite de scoring par minute. Merci de réessayer dans une minute.':
                                    time.sleep(30)   
                                    i-=1
                                else:
                                    df.append({'Url' : url, 'Keyword' : keyword[0], 'SOSEO yourtext_guru' : np.nan, 'DSEO yourtext_guru' : np.nan})
                            except:
                                try:                                                       
                                    soseo = driver.find_element("xpath", f'/html/body/div[2]/div/div[2]/div/div[12]/div/div/div[2]/table/tbody/tr[{nb}]/td[3]/button/strong').text
                                    soseo = float(soseo.strip('%') )
                                except:
                                    soseo = np.nan
                                #Dseo      
                                try:
                                    dseo = driver.find_element("xpath", f'/html/body/div[2]/div/div[2]/div/div[12]/div/div/div[2]/table/tbody/tr[{nb}]/td[4]/button/strong').text
                                    dseo = float(dseo.strip('%') )
                                except:
                                    dseo = np.nan
                                with self.data_lock:    
                                    df.append({'Url' : url, 'Keyword' : keyword[0], 'SOSEO yourtext_guru' : soseo, 'DSEO yourtext_guru' : dseo})                    
                        except:
                            pass
                            
                except Exception:
                    
                    pass

                    print('pass2')
        #print("J'affiche5",df)
        now_thread = time.time() 
        #app.update_progressBar('YourTextGuru', list_len, floor(now_thread - start_thread)/pool)




    def get_screaming_frog_info(self,res):
        random_file_name = str('test_file')

        #Ecriture des Urls dans un fichier afin qu'il puisse être crawler avec le Spider de Scrapy
        with open(f"./{random_file_name}.txt", 'w') as f:
            for item in list(set(res.get('Url'))):
                f.write("%s\n" % item)

        #Exécution du Spider de Scrapy dans un fichier JSON
        url = "./test_file.txt"
        config_sf="C:/Users/amohammedislam/Desktop/util DS/config-new.seospiderconfig"
        emplacement_sf=r"C:\Program Files (x86)\Screaming Frog SEO Spider\ScreamingFrogSEOSpiderCli.exe"
    
        save_crawl="."
        type_export="csv"
        subprocess.run([emplacement_sf, 
                        "--headless",            
                        "--save-crawl","--output-folder",save_crawl,
                        "--crawl-list",url,
                        "--export-format",type_export,               
                        "--export-tabs", 'Internal:All,Structured Data:All'
                        ])

        #Ouverture du fichier et récupération des informations dans un DataFrame
        time.sleep(5)
        df_scrapy = pd.read_csv('./internal_all.csv')
        df_struct = pd.read_csv('./structured_data_all.csv')


        #Supression du fichier JSON
        os.remove(f"./internal_all.csv")
        os.remove(f"crawl.seospider")
        os.remove(f"structured_data_all.csv")

        df_scrapy = df_scrapy.rename(columns={'Address': 'Url'})
        df_struct = df_struct.rename(columns={'Address': 'Url'})
        #Jointure des 2 DataFrames

        df = pd.merge(df_scrapy, df_struct, how='left', left_on = ['Url'], right_on = ['Url'])
        df = pd.merge(res, df, how='left', left_on = ['Url'], right_on = ['Url'])
            
        print("Crawler terminé.")
        return df



    def get_Data_as_csv(self,keyword,nb_sim_keywords,nb_links,nb_top_1):
        print('working on : ' +keyword)
        keywords_list = self.get_similar_keywords(keyword , nb_sim_keywords)
        print('step 01 done')
        red_df = self.find_URL_by_Keyword_SEMRUSH(keywords_list,nb_links)
        print('step 02 done')
        res_df = self.get_top(red_df,nb_top_1)
        print('step 03 done')
        res = res_df[ res_df['Url'].str.contains( '.gouv.fr')== False]
        print('step 04 done')
        print
        res = self.multiprocessing_function(1,res,self.get_babbarTech_scores, pool=1,name='BabbarTech')# Votre rate limit est de : 24 requêtes/minute that's why i am useing pool = 1 
        res.to_csv('./'+keyword+'.csv',index=False)
        print('step 05 done')
        res = self.multiprocessing_function(2,res,self.get_pageSpeed_scores_API, pool=20,name='PageSpeed')
        res = self.multiprocessing_function(3,res,self.get_pageSpeed_mobile_scores_API, pool=20,name='PageSpeed')
        res.to_csv('./'+keyword+'.csv',index=False)
        print('step 06 done') 
        res = self.multiprocessing_function(4,res,self.get_1fr_scores,pool=1, name='1fr')
        res.to_csv('./'+keyword+'.csv',index=False)
        print('step 07 done')
        res = self.multiprocessing_function(5,res,self.get_yourTextGuru_scores,pool=1, target=['Keyword','Url'],join=['Keyword','Url'],name='yourtext_guru')
        res.to_csv('./'+keyword+'.csv',index=False)
        print('step 08 done')
        df = self.get_screaming_frog_info(res)
        df.to_csv('./'+keyword+'.csv',index=False)
        print('step 09 done')
        sm = SemantiqueValues()
        df = sm.getSemantiqueValues(df)
        print('step 10 done')
        df.to_csv('./'+keyword+'.csv')
        print('step 10 done')


    def get_all_URL_data(self,df):
        t1 = Thread ( target = self.multiprocessing_function, args = (0, df ,self.get_babbarTech_scores,  1, ))
        t2 = Thread ( target = self.multiprocessing_function, args = (1, df ,self.get_pageSpeed_scores_API,  20, ))#PageSpeed
        t3 = Thread ( target = self.multiprocessing_function, args = (2, df ,self.get_pageSpeed_mobile_scores_API,  20, ))#PageSpeed
        t4 = Thread ( target = self.multiprocessing_function, args = (3, df ,self.get_1fr_scores,  5, ))#1fr
        t5 = Thread ( target = self.multiprocessing_function, args = (4, df ,self.get_yourTextGuru_scores,  5,['Keyword','Url'],['Keyword','Url'] ))#yourtext_guru

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        
        df = self.get_screaming_frog_info(df)
 
        return df

    def get_keywords(self,keyword):
        keywords_list = self.get_similar_keywords(keyword , 20) 
        return keywords_list



    def collect_data_for_all_urls_in_site(self, site_url, df, pool=1):
        # Récupérer le domaine du site
        site_domain = urlparse(site_url).netloc

        # Filtrer les URLs du même site
        site_urls = df[df['Url'].apply(lambda url: urlparse(url).netloc == site_domain)]['Url'].tolist()

        # Créer un DataFrame avec les URLs du site
        site_data = pd.DataFrame({'Url': site_urls})

        # Obtenir les données pour tous les URLs du même site
        site_data = self.get_all_URL_data(site_data, pool=pool)

        return site_data
    
  
    def get_Data_as_csv2(self,keyword,nb_sim_keywords,nb_links,nb_top_1):
        print("Debut de la collecte des données pour keyword") 
        keywords_list = self.get_similar_keywords(keyword , nb_sim_keywords) 
        red_df = self.find_URL_by_Keyword_SEMRUSH(keywords_list,nb_links)

        print(red_df)
        
        print(keywords_list)
        res_df = self.get_top(red_df,nb_top_1)
        
        res_df = res_df[ res_df['Url'].str.contains( '.gouv.fr')== False]
        
        t1 = Thread ( target = self.multiprocessing_function, args = (0,res_df ,self.get_babbarTech_scores,  1, ))
    
        t4 = Thread ( target = self.multiprocessing_function, args = (1,res_df ,self.get_1fr_scores,  2, ))#1fr
        t3 = Thread ( target = self.multiprocessing_function, args = (3,res_df ,self.get_pageSpeed_mobile_scores_API,  20, ))#PageSpeed
        t2 = Thread ( target = self.multiprocessing_function, args = (2,res_df ,self.get_pageSpeed_scores_API,  20, ))#PageSpeed
        
        t5 = Thread ( target = self.multiprocessing_function, args = (4,res_df ,self.get_yourTextGuru_scores,  1,['Keyword','Url'],['Keyword','Url'] ))#yourtext_guru
        t1.start()
        t4.start()
        t3.start()
        t5.start()
        t3.join()
        print("20% done")
        t2.start() 
        t1.join()
        print("40% done")
        t4.join() 
        print("60% done")
        t2.join()
        print("80% done")
        t5.join()
        print("90% done")

        # i am just faking this wroeting process i realy want to sleep
        
        df = res_df.copy()
        for i in range(5):
            if self.list_dfs[i] is not None:
                    df = pd.merge(df,self.list_dfs[i] , how='left', left_on = list(res_df.columns), right_on = list(res_df.columns)) 
        print(df)
        # Afficher toutes les colonnes
        print("Colonnes de df:", df.columns)
        # Afficher le nombre de colonnes
        print("Nombre de colonnes de df:", len(df.columns))

        df = self.get_screaming_frog_info(df)
        sm = SemantiqueValues()
        df = sm.getSemantiqueValues(df)
        path = './dataSETs/'+keyword+'.csv'
        df.to_csv(path)
         
        print('step 10 done') 
        
        

    def get_Data_as_csv3(self,start_url, keyword):
         
        
        red_list = self.get_all_site_urls(start_url)
        red_df = pd.DataFrame({'Url': red_list})
        red_df['Keyword'] = keyword

        print(red_df)
       #res_df = res_df[ res_df['Url'].str.contains( '.gouv.fr')== False]
        
        t1 = Thread ( target = self.multiprocessing_function, args = (0,red_df ,self.get_babbarTech_scores,  1, ))
    
        t4 = Thread ( target = self.multiprocessing_function, args = (1,red_df ,self.get_1fr_scores,  2, ))#1fr
        t3 = Thread ( target = self.multiprocessing_function, args = (3,red_df ,self.get_pageSpeed_mobile_scores_API,  20, ))#PageSpeed
        t2 = Thread ( target = self.multiprocessing_function, args = (2,red_df ,self.get_pageSpeed_scores_API,  20, ))#PageSpeed
        
        t5 = Thread ( target = self.multiprocessing_function, args = (4,red_df ,self.get_yourTextGuru_scores,  1,['Keyword','Url'],['Keyword','Url'] ))#yourtext_guru
        t1.start()
        t4.start()
        t3.start()
        t5.start()
        t3.join()
        print("20% done")
        t2.start() 
        t1.join()
        print("40% done")
        t4.join() 
        print("60% done")
        t2.join()
        print("80% done")
        t5.join()
        print("90% done")

        df = red_df.copy()
        for i in range(5):
            if self.list_dfs[i] is not None:
                    df = pd.merge(df,self.list_dfs[i] , how='left', left_on = list(red_df.columns), right_on = list(red_df.columns)) 
        print(df)

        chemin_du_fichier_csv = './dataSETs/resultats.csv'
        df.to_csv(chemin_du_fichier_csv, index=False)

       


    
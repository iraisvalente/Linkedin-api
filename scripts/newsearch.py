import requests
import sys
from bs4 import BeautifulSoup
import urllib.parse
import datetime
import argparse
import nltk
import spacy
import platform
import bs4 as bs
import urllib.request
import re
import nltk
import urllib.request
import heapq
import en_core_web_sm
from time import sleep

from spacy import displacy
from collections import Counter
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from os import getcwd, makedirs
from inscriptis import get_text
from nltk.tree import Tree
from collections import Counter
import webdriver_manager
import wikipedia


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome  import ChromeDriverManager
from selenium.webdriver import ActionChains

#def get_driver():
#    options = Options()
#    options.add_argument("start-maximized"); 
#    #options.add_argument("--headless"); 
#    options.add_argument("disable-infobars"); 
#    options.add_argument("--disable-extensions"); 
#    options.add_argument("--disable-gpu"); 
#    options.add_argument("--disable-dev-shm-usage"); 
#    options.add_argument("--no-sandbox");
#    options.add_experimental_option('excludeSwitches', ['enable-logging'])
#    
#    if platform.system() == 'Windows':
#        options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe" 
#
#    elif platform.system() == 'Linux':
#        options.binary_location = "/usr/bin/google-chrome"
#        
#    else:
#        print("""
#            [-] THIS SCRIPT ONLY WORKS WITH LINUX OR WINDOWS SYSTEMS, CONFIGURE FOR YOUR SYSTEM.
#            [-] TRY TO CONFIGURE WITH YOUR GOOGLE CHROME INSTALL PATH.
#        """)
#    
#    #driver = webdriver_manager.Chrome(service=Service(ChromeDriverManager().install()),options=options)
#    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
#    
#    return driver


def generate_google_search_url(*query):
    query= str(query[0]).split(" ")
    real_query=query[0]
    query= "+".join(x for x in query[1:])
    query= f"{real_query} {query}"
    nquery= f'{query}'
    #print(nquery)
    base_url = "https://www.google.com/search"
    params = {
        "q": nquery,
        "source": "hp",
    }
    url = base_url + "?" + urllib.parse.urlencode(params)
    #print(url)
    return url


def ImFeelLucky(*query):
    try:
        query=query[0].split(" ")
        real_query=query[0]
        query= "+".join(x for x in query[1:])
        query= f"{real_query} {query}"
        url=f"https://google.com/search?q={query}&btnI=I%27m+Feeling+Lucky&source=hp"
        #print(url)
        response=requests.get(url)
        link=response.text.split('a a <a href="')[1].split('"')[0]
        return link
    except :
        return ""


def search_name_in_list(sentences):
    names = []
    for sentence in sentences:
        nltk_results =  nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)))
        #print(nltk_results)
        for nltk_result in nltk_results:
            if type(nltk_result) == Tree:
                name = ''
                for nltk_result_leaf in nltk_result.leaves():
                    name += nltk_result_leaf[0] + ' '
                # print ('Type: ', nltk_result.label(), 'Name: ', name)
                if (nltk_result.label() == "PERSON"):
                    names.append(name)
    name_counts = Counter(names)
    most_common_name = name_counts.most_common(1)[0][0]
    return most_common_name


def clear_data_from_html_format(text):
    new_text = re.sub(r'\[[0-9]*\]', ' ', text)
    new_text = re.sub(r'\s+', ' ', new_text)
    return new_text



def get_resume(name:str, actually_driver=None):
    if actually_driver:
        driver = actually_driver
    #else:
    #    driver = get_driver()
    
    resume = ""
    try:
        wikipedia.set_lang("en")
        resume = wikipedia.summary(name, sentences=10)
    except:
        try:
            url = generate_google_search_url(name)+"&hl=en"
            driver.get(url)
            search_links = []
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            search_links = soup.find_all('div', class_="yuRUbf")

            for link in search_links:
                if "wikipedia" in link.a.get('href'):
                    resume = get_data_from_wikipedia(link.a.get('href'))
                    break
        except:
            print("[x] It was not possible to get information about the person.")
            resume = ""
    return resume
            

def get_data_from_wikipedia(url):
    
    url = url
    if url.startswith('https://es.wikipedia.org/'):
        url = url.replace("es.wikipedia.org", "en.wikipedia.org")
    
    if url.startswith('https://en.wikipedia.org/'):
        html  = urllib.request.urlopen(url).read().decode('utf-8')
        text = get_text(html)
        article_text = text
        article_text = article_text.replace("[ edit ]", "")
        article_text = clear_data_from_html_format(article_text)
        
        formatted_text = re.sub('[^a-zA-Z]', ' ', article_text)
        formatted_text = re.sub(r'\s+', ' ', formatted_text)
        
        #Tokerization
        sentence_list = nltk.sent_tokenize(article_text)
        
        # Words frecuently
        stopwords = nltk.corpus.stopwords.words('english')
        
        word_frequencies={}
        for word in nltk.word_tokenize(formatted_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] +=1
        
        
        maximum_frequency = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequency)
            
        # Calculate the most popular sentences
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        
        
        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)  
        
        summary = summary.replace(" .", ".")
        return summary      
    else:
        print("[x] It was not possible to get information about the person.")
        return ""
    
    
def get_linkedin_link(name:str="", company:str="", position:str="", links=[])->str:
    links_list = links
    linkedIn_link = ""
    is_correct_linkedin_link = False
    
    if name and company and position:
        linkedIn_link = ImFeelLucky(f"{name}+{company}+{position}+LinkedIn")
    
    elif not name and company and position:
        linkedIn_link = ImFeelLucky(f"{company}+{position}+LinkedIn")
    
    elif name and not company and not position:
        for try_get_linkedin_link in links_list:
            if "linkedin" in try_get_linkedin_link:
                linkedIn_link = try_get_linkedin_link
                break
        if not linkedIn_link:
            linkedIn_link=ImFeelLucky(f"{name}+LinkedIn")
    
    if name and linkedIn_link:
        name_list = str(name).lower().split(' ')
        for name_ in name_list:
            if name_ in linkedIn_link:
                is_correct_linkedin_link = True
                linkedIn_link = linkedIn_link

    if is_correct_linkedin_link:
        return linkedIn_link
    else:
        print("[x] The found a linkedin link valid")
        return ""
 
 

 
    
def make_search(**kwargs) -> str:
    
    driver = None
    kwargs_company = None
    kwargs_position = None
    kwargs_email = None
    kwargs_password = None
    kwargs_login  = None
    kwargs_name= None
    
    kwargs_index_tab = None
    
    if 'index_tab' in kwargs:
        kwargs_index_tab = int(kwargs['index_tab'])
    
    else:
        kwargs_index_tab = 1
        
    if 'driver' in kwargs:
        driver = kwargs['driver']
        driver.execute_script("window.open('', '_blank');")
        driver.switch_to.window(driver.window_handles[kwargs_index_tab])
        
        if 'login' in kwargs:
            kwargs_login = kwargs['login']
    #else:
    #    driver = get_driver()
    #    kwargs_login = 0
        
    if 'name' in kwargs:
        kwargs_name = kwargs['name']
        
    if 'company' in kwargs:
        kwargs_company = kwargs['company']
    
    if 'position' in kwargs:
        kwargs_position = kwargs['position']
    
    if 'email' in kwargs:
        kwargs_email = kwargs['email']
    
    if 'password' in kwargs:
        kwargs_password = kwargs['password']
    
    
    
       
    if kwargs_company and kwargs_position:
        URL = generate_google_search_url(f'{kwargs_company} {kwargs_position}')
    
    elif kwargs_name:
        URL = generate_google_search_url(f'{kwargs_name}')
    
    else:
        return {
            "status": 404,
            "info":{
                "name": "",
                "url": "",
                "description": ""
            }  
        }
    

    
    LIMIT_RESULTS_GOOGLE_SEARCH = 20

    links_list = [] 
    descriptions_list = [] 
    n_pages = 2    
    
    have_the_name = True
    name= ""
    linkstring= ""
    
    People_in_Linkedin = []
    About_in_Linkedin = []
    link_in_Linkedin = []
    
    people_togheter=""
    
    # First try to get info
    already_name =""
    already_link=""
    already_resume=""
    
    
    
    if kwargs_login == 1 or kwargs_login == "1":
        print("[-] Trying on login...")
        for page in range(1, n_pages):
            try:
                url = URL + "&start="+str((page - 1) * 10)+ "&hl=en"
                print(f"trying {url}")
                driver.get(url)        
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                search_links = soup.find_all('div', class_="yuRUbf")
                search_descriptions = soup.find_all('div', class_="Z26q7c UK95Uc")
                for link in search_links:
                    links_list.append(link.a.get('href'))
                    if "linkedin" in link.a.get('href').lower():
                        href=link.a.get('href')
                        print(f"Trying {href}")
                        driver.get(href)
                        sleep(7)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        potential_name=soup.find("h1",class_="text-heading-xlarge inline t-24 v-align-middle break-words").text
                        experience_positions = soup.find_all("span", {"class": "visually-hidden"})#.find('ul')
                        Complete_String=" "
                        Complete_String= " ".join(position.text for  position in experience_positions )
                        try:
                            This_position= Complete_String.split("Experience")[1].split(" · ")
                            if This_position == []:
                                This_position= Complete_String.split("Experiencia")[1].split(" · ")
                            This_position= " ".join(position for position in This_position)
                            this_position_in_a_list=This_position.upper().split(" ")
                        except:
                            pass
                        try:
                            This_About=Complete_String.split("About")[1].split("Activity")[0]
                        except:
                            pass
                        try:
                            position_in_a_list = kwargs_company.upper().split(" ")[1:]
                        except:
                            pass
                        
                        verify =  [x for x in position_in_a_list if x in this_position_in_a_list]
                        if len(verify) == len(position_in_a_list):
                            try:
                                People_in_Linkedin.append(potential_name)
                            except:
                                pass
                            try:
                                About_in_Linkedin.append(This_About)
                            except:
                                pass
                            try:
                                link_in_Linkedin.append(href)
                            except:
                                pass
                        
            except:
                pass
        if People_in_Linkedin != []:
            for i in range (0,len(People_in_Linkedin)):
                have_the_name = 1
                                
                try:
                    people_togheter += f"Name:  {People_in_Linkedin[i]}  \n"
                    already_name = People_in_Linkedin[i]
                except:
                    already_link =""
                try:
                    people_togheter += f"Link : {link_in_Linkedin[i]} \n"
                    already_link = link_in_Linkedin[i]
                    people_togheter += "\n\n\n"
                except:
                    already_link = ""
                try:
                    people_togheter += f"Resume:  {About_in_Linkedin[i]} \n"
                    already_resume = About_in_Linkedin[i]
                except:
                    already_resume = ""
                    
          
    
    
    if name == "" or already_name=="":
        print("Trying on error in loggin in or name not found")
        #links_list = [] 
        descriptions_list = [] 
        n_pages = 2    
        have_the_name = True
        name=""
        
        #driver = get_driver()
        driver.execute_script("window.open('', '_blank');")
        driver.switch_to.window(driver.window_handles[int(kwargs_index_tab)+1])       
        
        
        for page in range(1, n_pages):
            url = URL + "&start="+str((page - 1) * 10)+ "&hl=en"
            
            driver.get(url)
            print(url)
            try:
                name=driver.find_element(By.XPATH,"/html/body/div[6]/div/div[13]/div[1]/div[2]/div[2]/div/div/div[1]/div/block-component/div/div[1]/div[1]/div/div/div[1]/div/div/div[1]/div/div[1]/div[2]/div/div[1]/a")
                name= name.text
                print(f"{name} on first")
                if name.strip()=="":
                    1/0
                print(f"{name}")
            except:
                try:
                    name=driver.find_element(By.CLASS_NAME,"IZ6rdc")
                    name= name.text
                    print(f"{name} in second")
                    if name.strip()=="":
                        1/0
                    print(f"{name}")
                except:
                    try:
                        print("The name of the person is not found on the first page of google search.")
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        search_links = soup.find_all('div', class_="yuRUbf")
                        search_descriptions = soup.find_all('div', class_="Z26q7c UK95Uc")
                        linkstring=""
                        for link in search_links:
                            #print(link.a.get('href'))
                            links_list.append(link.a.get('href'))
                            linkstring+=link.a.get('href')
                        for description in search_descriptions:
                            descriptions_list.append(description.text)
                            linkstring+=description.text
                        driver.close()

                        links_caracteres = ["www", ".", "//", "/", "-", "_", "http", "https", ":","=","+","#","%","html"]
                        for each_caracter in links_caracteres:
                            linkstring = linkstring.replace(each_caracter, " ")

                        list_of_tokens=linkstring.split(' ')
                        list_of_tokens = [x for x in list_of_tokens if x != '']
                        list_of_tokens = [x.capitalize() for x in list_of_tokens if x != ' ']
                        linkstring=' '.join(c for c in list_of_tokens)
                        linkstring=''.join("" if c.isdigit() else c for c in linkstring)
                        nlp = en_core_web_sm.load()
                        tokens=nlp(linkstring)
                        people = [x for x in tokens.ents if x.label_.upper()=="PERSON"]
                        real_people =  [person for person in people if len(min(person.text.split(" "),key=len)) >2 ]
                        name=real_people[0]
                        print(f"{name}")
                    except Exception as e :
                        print("Can not find any name", e)
                        have_the_name=False
    
    
                
    if have_the_name:
        if already_name and already_link and already_link:
            info = {
                "status": 200,
                "info": {
                    "name": already_name,
                    "resume" : already_resume,
                    "link":  already_link
                }
            }
            print (info)
            return info
        else:
            print(get_full_info(name=name, company=kwargs_company, position=kwargs_position, links=links_list, driver=driver))
            return get_full_info(name=name, company=kwargs_company, position=kwargs_position, links=links_list, driver=driver)
        
    elif kwargs_name:
        print(get_full_info(name=kwargs_name, links=links_list, driver= driver))
        return get_full_info(name=kwargs_name, links=links_list, driver=driver)
    




def get_full_info(name:str="", company:str="", position:str="", links:list=[], driver=None)->dict:
    if name and company and position:
        return {
            "status": 200,
            "info": {
                "name": name,
                "resume" : get_resume(name, driver),
                "link":  get_linkedin_link(name, company, position, links)
            }
        }
    elif name and not company and not position:
        return {
            "status": 200,
            "info" : {
                "name": name,
                "resume" : get_resume(name, driver),
                "link":  get_linkedin_link(name, links)
            }
        }
    else:
        print("[x] Its necessary a name to search information.")
        return {
            "status": 404,
            "info":{
                "name": "",
                "resume" : "",
                "link": ""
            }
        }


     
    
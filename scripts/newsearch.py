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
import wikipedia
from selenium.webdriver.chrome.options import Options


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





def get_resume(name:str, driver):
    try:
        wikipedia.set_lang("en")
        print(wikipedia.summary(name, sentences=10))
    except:
        try:
            url = generate_google_search_url(name) + "&hl=en"
            driver.get(url)

            search_links = []

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            search_links = soup.find_all('div', class_="yuRUbf")

            for link in search_links:
                print(link.a.get('href'))
                if "wikipedia" in link.a.get('href'):
                    print(get_data_from_wikipedia(link.a.get('href')))
                    break
        except:
            print("It was not possible to get information about the person.")
            

    
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
        return "It was not possible to get information about the person."
    
    


def make_search(*args) -> str:
    print(args)
    driver=args[4]
    login = args[5]
    #args=args[0:2]
    arg=f'{args[0]} {args[1]}'
    #print(args)
    URL = generate_google_search_url(arg)
    LIMIT_RESULTS_GOOGLE_SEARCH = 20
    #options = Options()
    #options.add_argument("start-maximized"); 
    #options.add_argument("--headless"); 
    #options.add_argument("disable-infobars"); 
    #options.add_argument("--disable-extensions"); 
    #options.add_argument("--disable-gpu"); 
    #options.add_argument("--disable-dev-shm-usage"); 
    #options.add_argument("--no-sandbox");
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #if platform.system() == 'Windows':
    #    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe" #
    #
    #elif platform.system() == 'Linux':
    #    options.binary_location = "/usr/bin/google-chrome"
        
    #else:
    #    print("""
    #        THIS SCRIPT ONLY WORKINK WITH LINUX OR WINDOWS SYSTEM,
    #        PLEASE CONFIG FOR YOUR SYSTEM.
    #    """)
    #login = 1
    #print("Trying to log in")
    #try:
    #    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    #    driver.get("https://www.linkedin.com/")
    #    sleep(10)
    #    search_bar = driver.find_element(By.ID,"session_key")
    #    search_bar.clear()
    #    search_bar.send_keys("arturo@mobil.aullox.com")
    #    search_bar = driver.find_element(By.ID,"session_password")
    #    search_bar.clear()
    #    search_bar.send_keys(f"ohohdigoyo.1{Keys.RETURN}")
    #    sleep(15)
    #    #print("logged in")
    #except:
    #    #print("Not logged")
    #    login=0
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
    if login == 1 or login == "1":
        print("Trying on login")
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
                            position_in_a_list = args[0].upper().split(" ")[1:]
                        except:
                            pass
                        #print(potential_name)
                        #print(position_in_a_list)
                        #print(this_position_in_a_list)
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
                    people_togheter += "Name: " + People_in_Linkedin[i] + "\n"
                except:
                    pass
                try:
                    people_togheter += "Resume: " + About_in_Linkedin[i] + "\n"
                except:
                    pass
                try:
                    people_togheter += "Link : " + link_in_Linkedin[i] + "\n"
                    people_togheter += "\n\n\n"
                except:
                    pass
                #people_togheter +=  ";".join(x for x in link_in_Linkedin)
                print(people_togheter)
                return people_togheter
            #print(people_togheter)
            #sys.exit(0)                
    print("Trying on error in loggin in or name not found")
    links_list = [] 
    descriptions_list = [] 
    n_pages = 2    
    have_the_name = False
    name=""
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
            have_the_name=True
        except:
            try:
                name=driver.find_element(By.CLASS_NAME,"IZ6rdc")
                name= name.text
                print(f"{name} in second")
                if name.strip()=="":
                    1/0
                print(f"{name}")
                have_the_name=True
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
                    linkstring=linkstring.replace("www"," ")
                    linkstring=linkstring.replace("."," ")
                    linkstring=linkstring.replace("//"," ")
                    linkstring=linkstring.replace("/"," ")
                    linkstring=linkstring.replace("_"," ")
                    linkstring=linkstring.replace("https"," ")
                    linkstring=linkstring.replace("http"," ")
                    linkstring=linkstring.replace(":"," ")
                    linkstring=linkstring.replace("-"," ")
                    linkstring=linkstring.replace("="," ")
                    linkstring=linkstring.replace("+"," ")
                    linkstring=linkstring.replace("#"," ")
                    linkstring=linkstring.replace("%"," ")
                    linkstring=linkstring.replace("html"," ")
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
                    have_the_name=True
                except Exception as e :
                    print("Can not find any name", e)
                    have_the_name=False
    LINK_LINKEDIN = ""
    if have_the_name:
        get_resume(name, driver)
        #you need to get the biblio here
        ########Biblio=generate_google_search_url(f"{name}+{args[0]}+wikipedia")
        LinkedIn_link=ImFeelLucky(f"{name}+{args[0]}")
        # If I have the name and I have the Link ...
        # I will try validated the url with the name
        if name and  LinkedIn_link:
            have_the_link = False
            name_list = str(name).lower().split(' ')
            for name_ in name_list:
                if name_ in LinkedIn_link:
                    have_the_link = True
                    LINK_LINKEDIN = LinkedIn_link
                    print("Link: ", LINK_LINKEDIN)
                    #sys.exit(0)
        # If I have the name but I dont have the link ...
        # I will try get the Link
        linkedin_links_list = []
        if name and not LinkedIn_link:
            have_the_link = False
            for link_found in links_list:
                if "linkedin" in link_found:
                    linkedin_links_list.append(link_found)
            if len(linkedin_links_list) > 0:
                name_list = str(name).lower().split(' ')
                for name_ in name_list:
                    if not have_the_link:
                        for x_link in linkedin_links_list:
                            if name_ in x_link:
                                have_the_link = True
                                LINK_LINKEDIN = x_link
                                print("Link: ", LINK_LINKEDIN)
                                #sys.exit(0)
            #else:
            #    print("Can not find any link")
    # If  I dont have the name, but I have the link.
    # I will try get the name
    else:
        linkedin_links_list = []
        for link_found in links_list:
            if "linkedin" in link_found:
                linkedin_links_list.append(link_found)
                
        if len(linkedin_links_list) > 0:
            LinkedIn_link =  linkedin_links_list[0]
            print("url: ", LinkedIn_link)
            url_characteristics = ["www", "https", "http", "html"]
            if not name and LinkedIn_link:
                url_cleaned = re.sub(r'[^\w\s]', ' ', LinkedIn_link)
                for characteristic in url_characteristics:
                    url_cleaned = url_cleaned.replace(characteristic," ")
                list_of_tokens= url_cleaned.split(' ')
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
                get_resume(name, driver)
                LinkedIn_link=ImFeelLucky(f"{name}+{args[0]}")
                print(LinkedIn_link)
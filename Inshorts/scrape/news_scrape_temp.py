Asian_countries = [
  'Afghanistan',
  'Armenia',
  'Azerbaijan',
  'Bahrain',
  'Bangladesh',
  'Bhutan',
  'Brunei',
  'Cambodia',
  'China',
  'Cyprus',
  'Georgia',
  'India',
  'Indonesia',
  'Iran',
  'Iraq',
  'Israel',
  'Japan',
  'Jordan',
  'Kazakhstan',
  'Kuwait',
  'Kyrgyzstan',
  'Laos',
  'Lebanon',
  'Malaysia',
  'Maldives',
  'Mongolia',
  'Myanmar',
  'Nepal',
  'North Korea',
  'Oman',
  'Pakistan',
  'Palestine',
  'Philippines',
  'Qatar',
  'Russia',
  'Saudi Arabia',
  'Singapore',
  'South Korea',
  'Sri Lanka',
  'Syria',
  'Taiwan',
  'Tajikistan',
  'Thailand',
  'Timor-Lest',
  'Turkey',
  'Turkmenistan',
  'United Arab Emirates',
  'UAE',
  'Uzbekistan',
  'Vietnam',
  'Yemen'
]



import os, requests, re, string, random
from datetime import datetime, date
from bs4 import BeautifulSoup
from time import sleep


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm



def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def scrape(dated=str(date.today())):
    nlp = en_core_web_sm.load()

    categories = ['national', 'world', 'sports']
    news_dict = {
        'national': [], 
        'asia': [], 
        'world': [], 
        'sports': []
    }

    date_format = '%Y-%m-%d'
    from datetime import date
    today = str(date.today())
    times = (datetime.strptime(today, date_format) - datetime.strptime(dated, date_format)).days

    for category in categories:
        try:
            options = Options()
            options.add_argument('headless')
            options.add_argument('window-size=1200x600')

            url = 'https://www.inshorts.com/en/read/' + category
            driver = webdriver.Chrome(os.path.dirname(os.path.abspath('chromedriver')+'/chromedriver'), chrome_options=options)
            driver.implicitly_wait(100)
            
            driver.get(url)
        
            for i in range(2**(times+1)):
                button_click = driver.find_element_by_xpath('//*[@id="load-more-btn"]')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'load-more-btn')))
                webdriver.ActionChains(driver).move_to_element(button_click).click(button_click).perform()
                sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except requests.exceptions.RequestException:
            continue
        
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        news_cards = soup.find_all(class_='news-card')

        if not news_cards:
            continue
        
        for card in news_cards:
            try:
                date = card.find(class_='news-card-author-time').find(clas='date').text
                date_store = date.split(',')[0]
                date = datetime.strptime(date_store, '%d %b %Y').strftime('%Y-%m-%d')
                diff = (datetime.strptime(str(date), date_format) - datetime.strptime(str(dated), date_format)).days
                if date != dated:
                    if diff > 0:
                        continue
                    elif diff < 0:
                        break

            except AttributeError:
                date = None
            try:
                title = card.find(class_='news-card-title').find(class_='clickable').text
            except AttributeError:
                title = None
                
            try:
                content = card.find(class_='news-card-content').find('div').text
            except AttributeError:
                content = None
            
            news_content = {
                'id': randomString(20),
                'date': date_store,
                'content': content,
                'flag': 0
                # 'title': title
                
            }
            
            if news_content['date']==None or news_content['content']==None: #news_content['title']==None
                continue
            
            # news_content['title'] = re.sub('\'',"'",news_content['title'])
            # news_content['title'] = re.sub('\\n','',news_content['title'])
            
            news_content['content'] = re.sub('\'',"'",news_content['content'])
            news_content['content'] = re.sub('\\n','',news_content['content'])
            
            if category=='world':
              cat = 'world'
              S1 = set(Asian_countries)
              doc = nlp(news_content['content'])
              locs = set([X.text.lower() for X in doc.ents if X.label_=='LOC'])
              S2 = set(['asia'])
              if S2.intersection(locs):
                  #print(S2.intersection(locs))
                  cat = 'asia'
              
              gpes = set([X.text for X in doc.ents if X.label_=='GPE'])
              if S1.intersection(gpes):
                  cat = 'asia'
                  #print(S1.intersection(gpes))
                  news_dict[cat].append(news_content)
                  continue

            news_dict[category].append(news_content)
        driver.quit()
                

    for cat in news_dict:
        #news_dict[cat].sort(key=lambda x: datetime.datetime.strptime(x['date'], '%d %b %Y'), reverse=True)
        news_dict[cat] = news_dict[cat][0 : min(len(news_dict[cat]), 10)]
    
    
    # for cat in news_dict:
    #     print('\n\n\n\n'+cat.upper()+'\n')
    #     for news in news_dict[cat]:
    #         print(news)
    #         print()
    return news_dict
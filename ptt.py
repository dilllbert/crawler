import csv
import pathlib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options



def getpttcaturl():
    url = "https://www.ptt.cc/bbs/index.html"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'}

    res = requests.get(url,cookies = {'over18':'1'},headers=headers) 
    soup = BeautifulSoup(res.text,'html.parser') 

    cat_name =[item.text for item in soup.select('#main-container > div.b-list-container.action-bar-margin.bbs-screen > div > a > div.board-name')]
    cat_url = ['https://www.ptt.cc'+item.get('href') for item in soup.select('#main-container > div.b-list-container.action-bar-margin.bbs-screen > div > a')]

    cat ={
        'name' : cat_name,
        'url' : cat_url 
    }

    cat_df = pd.DataFrame(cat)

    try:
        cat_df.to_csv(str(pathlib.Path(__file__).parent.absolute())+"//cat.csv",encoding='utf_8_sig',index = False)
    except:
        print("123")

getpttcaturl()



#只找最新頁的
def getartitle():
            with open(str(pathlib.Path(__file__).resolve().parent)+'\\cat.csv', newline='',encoding='utf_8_sig') as csvfile:
                option = Options()
                option.add_argument("--headless")
                option.add_argument("--disable-notifications")
                option.add_argument('blink-settings=imagesEnabled=false')
                
                driverpath='geckodriver.exe'
                driver = webdriver.Firefox(executable_path=driverpath,options=option)

                rows = csv.DictReader(csvfile)

                titles = []
                urls = []
                cats = []

                for row in rows :
                        url =row['url']
                        catname = row ['name']
                        driver.get(url)

                        title =[item.get_attribute('textContent') for item in driver.find_elements(By.XPATH, '//*[@id="main-container"]/div[2]/div/div[2]/a')]
                        url =[item.get_attribute('href') for item in driver.find_elements(By.XPATH, '//*[@id="main-container"]/div[2]/div/div[2]/a')]

                        if (len(title) == len(url)):
                            urls = urls + url
                            titles = titles +title
                            cats = cats + [catname]*len(title)

                        
                cat ={
                    'catname' : cats,
                    'title':titles,
                    'url':urls
                }

                cat_df = pd.DataFrame(cat)

                try:
                    cat_df.to_csv(str(pathlib.Path(__file__).parent.absolute())+"//title.csv",encoding='utf_8_sig',index = False)
                except:
                    print("123")

                        
getartitle()



    

                
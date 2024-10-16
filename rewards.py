from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import math
import random

import requests
import json
from datetime import date, timedelta

profile_path = "C:\\Users\\zacma\\AppData\\Local\\Google\\Chrome\\User Data"
profile_name = "Default"

chrome_driver_path = "C:\\Users\\zacma\\Documents\\Chrome_Driver\\chromedriver.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={profile_path}")
chrome_options.add_argument(f"--profile-directory={profile_name}")
chrome_options.add_experimental_option("detach", True)

#ChromeDriver path
chrome_service = Service(executable_path=chrome_driver_path)

#Chrome browser
browser = webdriver.Chrome(service=chrome_service, options=chrome_options)


def getGoogleTrends(wordsCount: int, geo: str = 'US') -> list:
    searchTerms = []
    i = 0
    while len(searchTerms) < wordsCount:
        i += 1
        #Trends from google trends
        r = requests.get(
            f'https://trends.google.com/trends/api/dailytrends?hl=en&ed={(date.today() - timedelta(days=i)).strftime("%Y%m%d")}&geo={geo}&ns=15'
        )

        #If good response
        if r.status_code == 200:
            trends = json.loads(r.text[5:])
            for topic in trends["default"]["trendingSearchesDays"][0]["trendingSearches"]:
                searchTerms.append(topic["title"]["query"].lower())
                searchTerms.extend(
                    relatedTopic["query"].lower()
                    for relatedTopic in topic["relatedQueries"]
                )
            searchTerms = list(set(searchTerms))  #Remove duplicates
        else:
            print(f"Failed to retrieve trends: {r.status_code}")
            break

    #top wordsCount search terms
    return searchTerms[:wordsCount]

trends = getGoogleTrends(50)

for trend in trends:
    browser.get('https://www.bing.com/')

    assert 'Bing' in browser.title
    search_box = browser.find_element(By.NAME, 'q')
    search_box.send_keys(trend + Keys.RETURN)

    time.sleep(random.randint(3, 5))

browser.quit()

quit()
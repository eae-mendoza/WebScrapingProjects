from selenium import webdriver
from bs4 import BeautifulSoup as BS
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
import sys
import time
import csv


def get_listing(a):
    try:
        val = a.find('div',attrs={'class':'tm-marketplace-search-card__title'}).get_text()
        return val
    except:
        pass
        return 'No Name'

def get_price(a):
    try:
        val = a.find('div',attrs={'tm-marketplace-search-card__price'}).get_text()
        return val
    except:
        pass
        return 'No Price'
def get_buynow(a):
    try:
        val = a.find('div',attrs={'m-marketplace-search-card__price-right ng-star-inserted'}).get_text()
        return val
    except:
        pass
        return 'No Buy Now'

def get_closing(a):
    try:
        val = a.find('div',attrs={'tm-marketplace-search-card__time ng-star-inserted'}).get_text()
        return val
    except:
        pass
        return 'No Closing'

search = input("What do you want to look up in TradeMe\n")
max_page = input("How many pages do you want to browse?\n")
print(f'You chose to get {max_page} pages of results for {search}')

names  = []
prices = []
buy_nows = []
closing = []

driver = webdriver.Firefox()
url = 'https://www.trademe.co.nz/a/'
driver.get(url)
driver.find_element_by_xpath("//*[@id='search']").send_keys(f"{search}")
driver.find_element_by_xpath("/html/body/tm-root/div[1]/main/div/tm-dynamic-homepage/tm-homepage-search-header/nav/div[1]/tm-global-search/div/div[1]/form/button").send_keys(Keys.RETURN)
driver.find_element_by_xpath("/html/body/tm-root/div[1]/main/div/tm-dynamic-homepage/tm-homepage-search-header/nav/div[1]/tm-global-search/div/div[1]/form/button").click()
i=0
while i < int(max_page):
    try:
        time.sleep(4)
        r = driver.page_source
        html = BS(r, features='html.parser')
        stuffz = html.findAll('a', attrs={'class':'tm-marketplace-search-card__detail-section tm-marketplace-search-card__detail-section--link'})
        for stuff in stuffz:
            names.append(get_listing(stuff))
            prices.append(get_price(stuff))
            buy_nows.append(get_buynow(stuff))
            closing.append(get_closing(stuff))
        time.sleep(2)
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/tm-root/div[1]/main/div/ng-component/div/div/div/tg-row/tg-col/tm-search-results/div/div[2]/tm-potential-r18-content/div/tg-pagination/nav/ul/li[11]/tg-pagination-link/a'))))
        driver.find_element_by_xpath('/html/body/tm-root/div[1]/main/div/ng-component/div/div/div/tg-row/tg-col/tm-search-results/div/div[2]/tm-potential-r18-content/div/tg-pagination/nav/ul/li[11]/tg-pagination-link/a').click()
        i += 1
    except:
        pass
        i += 1


df = pd.DataFrame({'Product Name':names, 'Price': prices, 'Buy Now': buy_nows, 'Closing': closing})
df.to_csv(f'{search}.csv',index=False,encoding='utf-8')

print(df[0:20])

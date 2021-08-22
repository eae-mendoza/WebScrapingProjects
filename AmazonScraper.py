from selenium import webdriver
from bs4 import BeautifulSoup as BS
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import sys
import time

def get_price(a):
    if a != None:
        return a.get_text()
    else:
        return 'Cannot Buy'

def get_name(a):
    value = a.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
    value1 = a.find('span', attrs={'class': 'a-size-base-plus a-color-base a-text-normal'})
    if '<span' in str(value):
        if value != None:
            return value.get_text().strip()
        else:
            return 'No Product Name Available'
    else:
        if value1 != None:
            return value1.get_text().strip()
        else:
            return 'No Product Name Available'

def get_rating(a):
    value = a.find('div', attrs={'a-row a-size-small'})
    if value != None:
        return value.find('span').get_text().strip()
    else:
        return 'No Rating'

def search_parser(a):
    return a.replace(' ','+')



search = input("What do you want to look up in Amazon?\n")
max_page = input("How many pages do you want to browse?\n")
print(f'You chose to get {max_page} pages of results for {search}')

search_parsed=search_parser(search)

productname=[]
price=[]
rating=[]


driver = webdriver.Firefox()
url = f'https://www.amazon.com/s?k={search_parsed}&ref=nb_sb_noss'
driver.get(url)
i=0
#driver.find_element_by_xpath().click()
while (i < int(max_page)):
    try:
        time.sleep(2)
        r = driver.page_source
        time.sleep(2)
        html = BS(r, features='html.parser')
        stuffz = html.findAll('div', attrs={'data-component-type': 's-search-result'})
        for stuff in stuffz:
            productname.append(get_name(stuff))
            rating.append(get_rating(stuff))
            price.append(get_price(stuff.find('span', attrs={'class': 'a-offscreen'})))
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="a-last"]'))))
        driver.find_element_by_xpath('//*[@class="a-last"]').click()
        print("Navigating to Next Page")
        i+=1
        time.sleep(2)
    except (TimeoutException, WebDriverException) as e:
        print("Last page reached")
        break
driver.quit()

df = pd.DataFrame({'Product Name':productname, 'Price': price, 'Rating': rating})
df.to_csv(f'{search}.csv',index=False,encoding='utf-8')

print(df[0:20])
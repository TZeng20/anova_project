from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import time
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))

# Fill in your details here to be posted to the login form.
payload = {
    'inUserName': 'g1686359@nwytg.com',
    'inUserPass': 'qwertyuiop123'
}

base_url = 'https://www.funderbeam.com/startups?filter=%5B%7B%22key%22:%22LOCATION%22,%22value%22:%5B%22USA%22%5D,%22operator%22:%22IN%22%7D,%7B%22key%22:%22VALUATION%22,%22value%22:%221000000%22,%22operator%22:%22GREATER_OR_EQUAL_THAN%22%7D,%7B%22key%22:%22VALUATION%22,%22value%22:%2250000000%22,%22operator%22:%22LESS_OR_EQUAL_THAN%22%7D,%7B%22key%22:%22NEXT_FUNDING_DATE%22,%22value%22:%222%202018%22,%22operator%22:%22GREATER_OR_EQUAL_THAN%22%7D,%7B%22key%22:%22LAST_FUNDING_STAGE%22,%22value%22:%5B%22seed_round%22,%22angel_round%22,%22equity_crowdfunding%22,%22crowdfunding%22,%22series_x%22,%22series_a%22,%22series_b%22%5D,%22operator%22:%22IN%22%7D%5D'
login_url = 'https://www.funderbeam.com/login'

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.default_directory": dir_path+"/exits_csv",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
browser = webdriver.Chrome(chrome_options=options)
# Log in to Funderbeam
browser.get(login_url)
time.sleep(5)
browser.find_element_by_name('username').send_keys(payload['inUserName'])
time.sleep(2)
browser.find_element_by_name('password').send_keys(payload['inUserPass']+'\n')
time.sleep(5)

# Scrape investors page
browser.get(base_url)

headers = ['Name','Description','Industry','Keywords','Founded','Locations','Disclosed Funding','Next Round Estimate','Probability Score','Valuation Estimate']
data = pd.DataFrame(columns=headers)

try:
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="js-main-view-wrap"]/div/main/div[1]/div/div/button'))
    )
    element.click()
except:
    print('Timeout waiting for search to return results')
while True:
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    table = soup.find('div', {'class': 'tbody-group'})
    children = table.contents
    for child in children:
        if child == ' ':
            continue
        #df_row = pd.DataFrame(columns=headers)
        row = []
        i=0
        for col in child.contents:
            if col == ' ':
                continue
            if i == 0:
                # First col
                #print(col.div.div.a.div.text)
                row.append(col.div.div.a.div.text)
                i+=1
                # Description
                try:
                    #print(col.div.div.a.contents[2].text)
                    row.append(col.div.div.a.contents[2].text)
                except IndexError as e:
                    row.append('N/A')
            else:
                # All subsequent cols
                #print(col.div.string)
                row.append(col.div.string)
            i+=1
        df_row = pd.DataFrame([row],columns=headers)
        data = data.append(df_row, ignore_index=True)
    print(data)
    data = data.drop_duplicates()
    data.to_csv('funderbeam.csv')
    browser.implicitly_wait(6)
    browser.find_element_by_class_name('button-compact').click()
    browser.implicitly_wait(6)
    '''
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'grid-row'))
        )
    except:
        print('Timeout waiting for search to return results')'''
    #print(data)
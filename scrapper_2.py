# Import libraries and packages for the project 
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import csv
from selenium.webdriver.common.by import By

####
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
chrome_options.headless = True # also works

####


print('- Finish importing packages')

# Task 1: Login to Linkedin

# Task 1.1: Open Chrome and Access Linkedin login site
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
sleep(2)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('- Finish initializing a driver')
sleep(2)

# Task 1.2: Import username and password
#credential = open('credentials.txt')
#line = credential.readlines()
username = "garciawork3232@gmail.com"
password = "l8hMP9s#7P3o"
print('- Finish importing the login credentials')

sleep(5)

# Task 1.2: Key in login credentials
email_field = driver.find_element(By.ID , 'username')
email_field.send_keys(username)
print('- Finish keying in email')
sleep(3)

password_field = driver.find_element(By.NAME,'session_password')
password_field.send_keys(password)
print('- Finish keying in password')
sleep(2)

# Task 1.2: Click the Login button
signin_field = driver.find_element(By.XPATH , '//*[@id="organic-div"]/form/div[3]/button')

sleep(3)
signin_field.click()

if requests.get(url).status_code == 200:
    print('- Finish accessing the login page')
else:
    print('- Fail to access the login page')

sleep(3)

print('- Finish Task 1: Login to Linkedin')

search_profile = input('What profile do you want to scrape? ')

driver.get(search_profile)
pageSource = driver.page_source
soup = BeautifulSoup(pageSource, 'html.parser')

info_profile = {}
title_profile = soup.find('div', class_='artdeco-entity-lockup__title ember-view')

if title_profile:
    only_text_title_profile = re.sub(r'\n+', '', title_profile.text)
    x = only_text_title_profile.split()
    info_profile['title_name'] = x

sections_profile = soup.find_all('section', class_='artdeco-card')

for i in sections_profile:
    item_key = i.find('span', {'class': 'visually-hidden'})

    if item_key:
        info_profile[item_key.text] = []

    item_value = i.find('ul', {'class': 'pvs-list'})
    if item_value:
        for j in item_value.find_all('li'):
            span_text = j.find('span', {'class': 'visually-hidden'})
            if span_text:
                only_text = re.sub(r'\n+', '', span_text.text)
                info_profile[item_key.text].append(only_text)

print(info_profile)

#print (soup.prettify())
#fileToWrite = open("page_source.html", "w")
#fileToWrite.write(pageSource)
#fileToWrite.close()
#fileToRead = open("page_source.html", "r")
#print(fileToRead.read())
#fileToRead.close()
driver.quit()

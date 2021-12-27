from os import times
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
import time

## TODO

# chrome_drive_path = 'c:\\Users\\user\\Downloads\\chromedriver_win32\\chromedriver.exe'


def get_token():

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--disable-dev-shm-usage')
    chromeOptions.add_argument('ignore-certificate-errors') 
    browser = webdriver.Chrome(chrome_drive_path,options=chromeOptions)
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow'}}
    browser.get('https://rent.591.com.tw/?shType=clinch&order=money&orderType=asc&kind=1&region=1') 
    
    time.sleep(3)

    soup = BeautifulSoup(browser.page_source,"lxml") 
    csrf = soup.find("meta", {"name":"csrf-token"})['content']

    for c in browser.get_cookies():
        if c['name'] == 'XSRF-TOKEN':
            xsrf = c['value']
        if c['name'] == '591_new_session':
            new_sec = c['value']

    browser.quit()
    return csrf, xsrf, new_sec







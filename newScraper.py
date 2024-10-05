import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

PROXY = '88.198.212.91:3128'

service = Service()
chrome_option = webdriver.ChromeOptions()
chrome_option.add_argument(f'--proxy-server={PROXY}')

driver = webdriver.Chrome(service=service, 
                          options=chrome_option)
driver.get('https://www.myip.com/')

time.sleep(100)

#2804:14c:5bc1:8acb:2507:7b76:5cae:4729
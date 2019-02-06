import csv 
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# first page (TASK: need to iterate)
url = "https://www.sephora.com/product/alpha-beta-r-peel-extra-strength-daily-peel-mini-P425868?icid2=products%20grid:p425868:product"
# opens up url in Google Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml') 
soup.prettify()

product_info = soup.find("div", {"class":"css-19965sg"})
brand = list(product_info.children)[0].next_element.next_element.text
product = list(product_info.children)[0].next_element.next_sibling.text

description = soup.find("div", {"class": "css-1vwy1pm"}).get_text()
print(description, type(description))
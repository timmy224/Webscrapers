# https://www.upcitemdb.com/

#
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import keys
from bs4 import BeautifulSoup

"""
# only need if IP ban possible
from time import sleep
from random import randint

from IPython.core.display import clear_output
from warnings import warn
"""

# Requests module downloads webpage
print("Enter website")
enter_website = input("> ")
print("What is the brand name?")
answer = input("> ")


# UPCitemDB.com doesn't seem to have working page links for products
# IGNORE: UPCitemDB seems to only have a max of 5 pages
pages = [str(i) for i in range(6)]

# creates CSV file to write UPC and Product name into
file_csv = csv.writer(open('UPCitemDB_{}.csv'.format(answer), 'w'))
file_csv.writerow(['UPC', 'Product Name'])

webpage = requests.get(enter_website)

# prints whether scraper is working
if webpage.status_code == 200:
    print("Page downloaded successfully")
else: 
    print("Error downloading page")

# print(webpage.content)

# Beautifulsoup module parses document and extraction
soup = BeautifulSoup(webpage.content, 'html.parser')
soup.prettify()

# finds all HTML class = 'rImage" tags (UPC and Product Name nested in here)
for stuff in soup.find_all(class_="rImage"):
    important_text = stuff.get_text()
    UPC = important_text[:12]
    Product_name = important_text[12:]

    # writes to CSV file; see line 25 to 27
    file_csv.writerow([UPC, Product_name])

"""
ONLY NEEDED IF IPBAN POSSIBLE

# avoid IP address ban (slows request rate)
for _ in range(5):
    print("Preventing IP address ban")
    sleep(randint(1,3))

start_time = time()
requests = 0

for _ in range(5):
    requests += 1
    sleep(randint(0,5))
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)

warn("Scrape didn't finish")
"""


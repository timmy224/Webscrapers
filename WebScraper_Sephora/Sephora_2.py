import csv 
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# first page (TASK: need to iterate)
url = "https://www.sephora.com/search?keyword=skincare&pageSize=5&currentPage=709"

# opens up url in Google Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
# --incognito
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

# closes Sephora sign-in pop up window

popUp_close = driver.find_element_by_class_name("css-ll28en").click()
time.sleep(3)

"""
def next_button_exist():
    WebDriverWait(driver, 5)
    
    next_button_xpath = "//*[name()='path' and @d='M57 142.5L9.5 95 0 104.5l38 38-38 38 9.5 9.5L57 142.5z']//../.."
    if driver.find_element_by_xpath(next_button_xpath).get_attribute("disabled"):
        print("Button disabled")
        #print("This is the last page!")
        #driver.quit()
        
    else: 
        print("Button enabled")
        #print("Next button found")
        #driver.driver.find_elements_by_xpath("//*[name()='path' and @d='M57 142.5L9.5 95 0 104.5l38 38-38 38 9.5 9.5L57 142.5z']//../..").click()
        ## driver.find_element_by_class_name("css-xswd36").click()
        #get_info()
"""

def next_button_exist():
    WebDriverWait(driver, 5)
    
    next_button_xpath = "//*[name()='path' and @d='M57 142.5L9.5 95 0 104.5l38 38-38 38 9.5 9.5L57 142.5z']//..//../following-sibling::button[last()]"
    if driver.find_element_by_xpath(next_button_xpath).get_attribute("disabled"):
        print("Button disabled")
        #print("This is the last page!")
        time.sleep(3)
        driver.quit()
        
    else: 
        print("Button enabled")
        print("Next button found")
        driver.find_element_by_xpath(next_button_xpath).click()
        ## driver.find_element_by_class_name("css-xswd36").click()
        #get_info()
        time.sleep(3)
        get_info()
        

def get_info():

    soup = BeautifulSoup(driver.page_source, 'lxml') 
    soup.prettify()

    # scroll
    body_elem = driver.find_element_by_tag_name("body")

    no_of_pagedowns = 7

    while no_of_pagedowns:
        body_elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1

    list_links = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//a[contains(@href,'/product/')]")]

    checked_links = []
    for link in list_links:
        print(link)
        
        driver.get(link)
        driver.back()
        """
        if link != set(checked_links):
            driver.get(link)
            driver.back()
        else: 
            break
        """

    # driver.find_element_by_class_name("css-1be47h1").click()
    time.sleep(1)
    next_button_exist()
    
get_info()



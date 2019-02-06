import csv
import time # switch to wait until element appears for learning
import os # used for sleep after script finishes 
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys   
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome(options=chrome_options)

url = 'https://sokoglam.com/collections/skincare?page=1'

driver.get(url)

WebDriverWait(driver, 5)

def getCurrentPageListOfLinks():
    
    global list_of_links

    list_of_links = []

    products = driver.find_elements_by_xpath('//h2[@class="product__title"]//a[starts-with(@href, "/products/")]')

    count = 0 
    for each_product in products:
        ind_link = each_product.get_attribute('href')
        list_of_links.append(ind_link)
        count += 1 
        print(count, '', ind_link)
    
    #print(list_of_links)
    return list_of_links

def productInfo():

    for each in list_of_links:
        driver.get(each)

        WebDriverWait(driver, 10)

        url_link = driver.current_url

        brand_name_xpath = '//p[@class="vendor"]//child::a'
        brand_name = driver.find_element_by_xpath(brand_name_xpath).text

        product_name_xpath = '//h1[@class="h2"]'
        product_name = driver.find_element_by_xpath(product_name_xpath).text

        image_xpath = '//img[@class="zoom"]'
        image_link = driver.find_element_by_xpath(image_xpath).get_attribute('src')

        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            ingredients_xpath_click = '//a[@class="fancy-trigger"]'
            driver.find_element_by_xpath(ingredients_xpath_click).send_keys(Keys.RETURN)

            ingredients_p_xpath = '//div[@id="full-ingredients"]//following::p'
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ingredients_p_xpath)))
            ingredients = (driver.find_elements_by_xpath(ingredients_p_xpath))[0].text

        except NoSuchElementException:
            ingredients = ""
            print('')

        except TimeoutException:
            ingredients = ""
            print('')

        print(brand_name, product_name, ingredients, image_link, url_link)
        file_csv.writerow([brand_name, product_name, ingredients, image_link, url_link])

        driver.back()

        WebDriverWait(driver, 5)

def checkNextButton():

    global next_button_status
    next_button_status = True

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    
    try: 
        close_PopUp = driver.find_element_by_xpath('//a[@title = "Close"]')
        close_PopUp.click()

        WebDriverWait(driver, 3)
    
    except NoSuchElementException:
        print('No Pop-Up detected')
        pass

    try:
        next_button = driver.find_element_by_xpath('//a[. = "Next »" ]')
        next_button.click()

    except NoSuchElementException:
        print('--- Last page! ---')
        next_button_status = False
        return next_button_status

with open('Sokoglam_{}.csv'.format(date.today()), 'w') as f:

    file_csv = csv.writer(f)
    file_csv.writerow(['Brand', 'Product Name', 'Ingredients', 'Image Link', 'URL Link'])

    while True:
        getCurrentPageListOfLinks()
        productInfo()
        checkNextButton()
        WebDriverWait(driver, 10)
        
        if next_button_status == False: 
            print('File created: Sokoglam_{}.csv'.format(date.today()))
            break
            
        else:
            print('--- Next Page! ---')

# os.system('pmset sleepnow') # command for sleep after script finishes






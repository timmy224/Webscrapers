import csv
import time
import os
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import TimeoutException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.target.com/c/hair-color-care-beauty/-/N-5xu0h'


driver.get(url)

def lazyLoadScroll():
    """ scrolls down entire webpage to let all products load """
    
    time.sleep(5)

    bodyElem = driver.find_element_by_tag_name('body')
    no_of_pagedowns = 45

    while no_of_pagedowns:
        bodyElem.send_keys(Keys.PAGE_DOWN)
        no_of_pagedowns -= 1

def getListofLinks():
    """ gets list of all products on current page """
    global list_of_links 
    list_of_links = []

    product_links_xpath = '//h3[@class="Col-favj32-0 kIqrCB"]//child::a'
    products = driver.find_elements_by_xpath(product_links_xpath)
    
    count = 0
    for each_product in products:
        ind_link = each_product.get_attribute('href')
        list_of_links.append(ind_link)
        count += 1
        print(count, ind_link)
    
    #print(list_of_links)
    return list_of_links

def productInfo():
    """ gets brand name, product name, ingredients, and product image """
    
    for each in list_of_links:
        driver.get(each)

        try:
            brandName_xpath = '//div[@class="styles__ProductDetailsTitleRelatedLinks-sc-12eg98-0 eVTLYK"]//span'
            brandName_origText = driver.find_element_by_xpath(brandName_xpath).text
            brandName = brandName_origText[9:]
        except NoSuchElementException:
            brandName = ''

        try:
            productName_xpath = '(//h1[@class="h-margin-b-none h-margin-b-tiny h-text-normal h-margin-t-default sc-bdVaJa ixexCJ"]//span)[1]'
            productName_loc = driver.find_element_by_xpath(productName_xpath)
            productName = productName_loc.text
        except NoSuchElementException:
            productName = ''

        #def ingredients():
            #""" looks for drug facts link to click, then looks for active/inactive ingredients text """

        #product_bodyElem = driver.find_element_by_tag_name('body')
        #product_bodyElem.send_keys(Keys.PAGE_DOWN) 

        try: 
            driver.find_element_by_xpath('//*[@id="tab-Drugfacts"]').click()
            try:
                active_ingredients_xpath = '//h4[text()[contains(., "Active ingredients")]]/..'
                active_ingredients_all = driver.find_element_by_xpath(active_ingredients_xpath).get_attribute('textContent')
                active_ingredients = 'Active ingredients: ' + active_ingredients_all[18:]
            except NoSuchElementException:
                active_ingredients = ''
            try:
                inactive_ingredients_xpath = '//h4[text()[contains(.,"Inactive ingredients")]]/..'
                inactive_ingredients_all = driver.find_element_by_xpath(inactive_ingredients_xpath).get_attribute('textContent')
                inactive_ingredients = 'Inactive ingredients: ' + inactive_ingredients_all[19:]
            except NoSuchElementException:
                inactive_ingredients = ''

            ingredients = active_ingredients + inactive_ingredients

        except NoSuchElementException:
            ingredients = ''

        product_url = driver.current_url

        #return ingredients
        #ingredients()
        
        try:
            image_xpath = '(//img[contains(@src, "//target.scene7.com/is/image/Target/GUEST")])[1]'
            product_image = driver.find_element_by_xpath(image_xpath).get_attribute('src')
        except NoSuchElementException:
            product_image = ''

        print(brandName, productName, ingredients, product_image, product_url)
        file_csv.writerow([brandName, productName, ingredients, product_image, product_url])
        
        driver.back()
        time.sleep(5)

def checkNextButton():
    """ checks for next button and clicks """
    
    #driver.back()
    #time.sleep(5)

    try:
        nextPageBtn_xpath = '//div[@class="h-display-flex h-flex-align-center h-flex-justify-center"]//a[@aria-label="next page"]'
        nextPageBtn = driver.find_element_by_xpath(nextPageBtn_xpath)
        driver.execute_script("arguments[0].scrollIntoView();", nextPageBtn)
        nextPageBtn.click()
    
    except NoSuchElementException:
        print('Next button not found')
        return False

with open('Target_Haircare_Color_{}.csv'.format(date.today()), 'w') as f:

    file_csv = csv.writer(f)
    file_csv.writerow(['Brand', 'Product Name', 'Ingredients', 'Product Image'])

    page_number = 0
    while True:
        page_number += 1
        print('Page number: {}'.format(page_number))
        lazyLoadScroll()
        getListofLinks()
        productInfo()
        lazyLoadScroll()
        checkNextButton()

os.system('pmset sleepnow') # sleeps computer after script finishes


# scrollUntilNoNewElements() generates a list of weblinks for all products.
# productInfo() goes through each link, gets product info, and writes to file. 

import csv
import time
from datetime import date
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 

url="https://reissue.co/search"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('window-size=1200x600')

driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

time.sleep(3)

def scrollUntilNoNewElementsWithContinuousSave():
    """ same as scrollUntilNoNewElements() but with continuous save"""

    time.sleep(5)

    SCROLL_PAUSE_TIME = 5
    
    last_height = driver.execute_script("return document.body.scrollHeight")

    old_num_of_links = len(driver.find_elements_by_xpath("//a[contains(@href, '/product/')]"))

    global list_links

    list_links = []

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        new_num_of_links = len(driver.find_elements_by_xpath("//a[contains(@href,'/product/')]"))

        if new_height == last_height:
            print('\n', "done scrolling", '\n')

            if new_num_of_links == old_num_of_links:
                print('\n', 'no new links', '\n')
                break

            else:
                list_of_website_links = driver.find_elements_by_xpath("//a[contains(@href,'/product/')]")
                                                
                for link in list_of_website_links[old_num_of_links:new_num_of_links + 1]:
                    ind_link = link.get_attribute('href')  
                    list_links.append(ind_link)
                    print(ind_link)

        else:
            list_of_website_links = driver.find_elements_by_xpath("//a[contains(@href, '/product/')]")

            for link in list_of_website_links[old_num_of_links:new_num_of_links + 1]:
                ind_link = link.get_attribute('href')  
                list_links.append(ind_link)
                print(ind_link)

        last_height = new_height
        old_num_of_links = new_num_of_links

    print('final link list', list_links)
    return list_links

def productInfo(list_from_scroll):
    """ gets item link, brand, name, ph, ingredients, and product image """

    with open('Reissue_{}.csv'.format(date.today()), 'w') as f:
        file_csv = csv.writer(f)
        file_csv.writerow(['Brand', 'Product Name', 'pH', 'Ingredients', 'Image Link', 'Item Link'])

        for each in list_from_scroll:
            driver.get(each)

            time.sleep(5)
            
            # item, brand, title, ph
            item_link = driver.current_url
            product_brand = driver.find_element_by_class_name('productPage__brand').text
            product_title = driver.find_element_by_class_name('productPage__name').text
            ph_level = driver.find_element_by_xpath("//text()[. = 'PH Level']/following::p").text

            # ingredients
            try:
                driver.find_element_by_class_name("notableIngredients__view-all").click()
                time.sleep(5)
                ingredients = driver.find_element_by_xpath("//text()[. = 'Full ingredients']/following::p").text 
            
            except NoSuchElementException:
                ingredients = ""
                pass

            # image
            image_link = driver.find_element_by_class_name('productPage__img').get_attribute('src')

            print(item_link, product_brand, product_title, ph_level, ingredients, image_link, "")

            file_csv.writerow([product_brand, product_title, ph_level, ingredients, image_link, item_link])

productInfo(scrollUntilNoNewElementsWithContinuousSave())

print('File created: ', 'Reissue_{}.csv'.format(date.today()))
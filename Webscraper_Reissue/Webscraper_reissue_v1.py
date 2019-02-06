# adjust time.sleep() depending on browser webpage load

import csv
import time
from datetime import date
from selenium import webdriver

url="https://reissue.co/search"
# url='https://reissue.co/product/the-ordinary-niacinamide-10----zinc-1-'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

time.sleep(3)

with open('Reissue_{}.csv'.format(date.today()), 'w') as f:
    file_csv = csv.writer(f)
    file_csv.writerow(['Brand', 'Product Name', 'pH', 'Ingredients',
                       'Image Link', 'Item Link'])

def scrollUntilNoNewElements():

    time.sleep(3)

    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("done scrolling")
            break
        last_height = new_height

def getProductLinks():
    """ gets link for all products from search page """

    time.sleep(2)

    # list_links = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//a[contains(@href,'/product/')]") ]
    # print(list_links)

    list_links = []

    for link in driver.find_elements_by_xpath("//a[contains(@href, \
                                              '/product/')]"):
        ind_link = link.get_attribute('href')
        list_links.append(ind_link)
        # print(ind_link)
    return list_links
    
def scrollUntilNoNewElementsWithContinuousSave():
    """ same as scrollUntilNoNewElements() but with continuous save"""

    time.sleep(3)

    SCROLL_PAUSE_TIME = 3
    
    last_height = driver.execute_script("return document.body.scrollHeight")

    old_num_of_links = len(driver.find_elements_by_xpath("//a[contains(@href, \
                                                '/product/')]"))

    global list_links

    list_links = []

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        new_num_of_links = len(driver.find_elements_by_xpath("//a[contains(@href, \
                                            '/product/')]"))

        if new_height == last_height:
            print('\n', "done scrolling", '\n')

            if new_num_of_links == old_num_of_links:
                print('\n', 'no new links', '\n')
                break

            else:
                list_of_website_links = driver.find_elements_by_xpath("//a[contains(@href, \
                                                '/product/')]")
                                                
                for link in list_of_website_links[old_num_of_links:new_num_of_links + 1]:
                    ind_link = link.get_attribute('href')  
                    list_links.append(ind_link)
                    print(ind_link)

        else:
            list_of_website_links = driver.find_elements_by_xpath("//a[contains(@href, \
                                                '/product/')]")

            for link in list_of_website_links[old_num_of_links:new_num_of_links + 1]:
                ind_link = link.get_attribute('href')  
                list_links.append(ind_link)
                print(ind_link)

        last_height = new_height
        old_num_of_links = new_num_of_links

    print('final link list', list_links)
    return list_links

def productInfo():
    """ gets item link, brand, name, ph, ingredients, and product image """

    for each in list_links:
        driver.get(each)

        time.sleep(3)
        
        # item, brand, title, ph
        item_link = driver.current_url
        product_brand = driver.find_element_by_class_name('productPage__brand').text
        product_title = driver.find_element_by_class_name('productPage__name').text
        ph_level = driver.find_element_by_xpath("//text()[. = 'PH Level']\
                                                /following::p").text

        # ingredients
        driver.find_element_by_class_name("notableIngredients__view-all").click()
        ingredients = driver.find_element_by_xpath("//text()[. = \
                                            'Full ingredients']/following::p").text 

        # image
        image_link = driver.find_element_by_class_name('productPage__img')\
                                                            .get_attribute('src')

        print(item_link, product_brand, product_title, ph_level, ingredients, 
            image_link, "")

        file_csv.writerow([product_brand, product_title, ph_level, ingredients, 
                        image_link, item_link])
    

scrollUntilNoNewElementsWithContinuousSave()
productInfo()

print('File created: ', 'Reissue_{}.csv'.format(date.today()))
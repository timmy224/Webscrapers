# import necessary modules
import csv
import time
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

# create CSV file (for later write)
file_csv = csv.writer(open('Origins.csv', 'w'))
file_csv.writerow(['Product Name', 'Product Subheading', 'Recommended Skin Type', 'Details',
                   'Ingredients', 'Item Link'])

# get to origins website
url = 'https://origins.com/'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')

driver = webdriver.Chrome(chrome_options = chrome_options)
driver.get(url)
time.sleep(2)

# close pop up window
def popUp_check():
    if driver.find_element_by_id('cboxClose'):
        driver.find_element_by_id('cboxClose').click()
    else:
        pass

# click on skincare tab
skincare_tab = '//*[@id="node-1288"]/div/div/ul/li[2]/span'
skincare_tab_click = driver.find_element_by_xpath(skincare_tab)
ActionChains(driver).move_to_element(skincare_tab_click).perform()

# get list of categories under skincare
category_list_xpath = '//*[@class="menu__list menu__list--lvl-1 list-split list-split--2"]'
driver.find_element_by_xpath(category_list_xpath)

# doesn't include the links to access 'Best For Men' and 'Sun Protection'
cat_links = driver.find_elements_by_xpath('//a[contains(@href, "/products/")]')

new_list = []
for link in cat_links:
    new_list.append(link.get_attribute('href'))

trunc_cat_list = new_list[:9]

best_for_men = driver.find_element_by_xpath('//a[contains(@href, "/best-men-skincare")]')
sun_protection = driver.find_element_by_xpath('//a[contains(@href, "/sun-protection-skincare")]')

trunc_cat_list.append(best_for_men.get_attribute('href'))
trunc_cat_list.append(sun_protection.get_attribute('href'))

def ind_category():
    body_elem = driver.find_element_by_tag_name('body')
    no_of_pagedowns = 8

    while no_of_pagedowns:
        body_elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns -= 1

    # generate list of products on category page
    product_links = driver.find_elements_by_xpath('//a[contains(@href,"/product/")]')
    product_list = []

    for product in product_links:
        product_list.append(product.get_attribute('href'))
    
    product_list = product_list[::4]
      
    def product_content():
        try:
            for each_product in product_list:
                driver.get(each_product)
                
                item_link = driver.current_url

                product_name_class = 'product-full__name'
                product_name = driver.find_element_by_class_name(product_name_class).text
                # print(product_name); maybe remove TM symbol

                product_subheading_class = 'product-full__subheading'
                product_subheading = driver.find_element_by_class_name(product_subheading_class).text

                rec_skintype_class = 'product-full__attributes-skintype'
                rec_skintype_raw = driver.find_element_by_class_name(rec_skintype_class).text
                rec_skintype = rec_skintype_raw[17:]

                # details
                details_xpath = '//div[@class="product-full__overview product-full__tabbed-content js-product-full__tabbed-content current"]'
                details = driver.find_element_by_xpath(details_xpath).text

                # ingredients
                ingredients_tab_click = '//li[@data-tab-content="ingredients"]'
                driver.find_element_by_xpath(ingredients_tab_click).click()
            
                ingredients_tab = '//div[@class="product-full__overview product-full__tabbed-content js-product-full__tabbed-content current"]'
                ingredients = driver.find_element_by_xpath(ingredients_tab).text
            
                print(product_name, product_subheading, '\n')

                # write to CSV file with product info
                file_csv.writerow([product_name, product_subheading, rec_skintype, details, ingredients, item_link])

        except:
            pass

    product_content()

popUp_check()

for each_category in trunc_cat_list:
    driver.get(each_category)
    ind_category()
    
# for loop that goes through each category
    # get a list of links for each product
    # for loop through this list to access product page
        # grab product info 
            # item link
            # product name
            # product subheading
            # recommended skintype
            # details
            # ingredients
        # write to CSV file with product info
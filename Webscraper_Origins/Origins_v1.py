import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

file_csv = csv.writer(open('Origins.csv', 'w'))
file_csv.writerow(['Product Name', 'Product Sub', 'Skin Type', 'Details', 'Ingredients', 'Item Link'])

url = "https://www.origins.com/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options = chrome_options)
driver.get(url)

time.sleep(3)
# close pop up
def popUp_check():
    if driver.find_element_by_id("cboxClose"):
        driver.find_element_by_id("cboxClose").click()
    else:
        pass

popUp_check()

def category_pages():
    body_elem = driver.find_element_by_tag_name('body')
    no_of_pagedowns = 8

    while no_of_pagedowns:
        body_elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns -= 1 

    # gets the links for categories under skincare tab: moisturizers, face cleansers, etc. 
    list_links = [link.get_attribute('href') for link in \
        driver.find_elements_by_xpath('//a[contains(@href,"/product/")]')]

    def product_content():
        soup = BeautifulSoup(driver.page_source, 'lxml')
        soup.prettify()

        # getting content
        item_link = driver.current_url
        product_name = driver.find_element_by_class_name('product-full__name').text
        product_subheading = driver.find_element_by_class_name('product-full__subheading').text
        
        # remove 'recommended for:' text
        rec_skintype_raw = driver.find_element_by_class_name('product-full__attributes-skintype').text
        rec_skintype = rec_skintype_raw[17:]

        # Method #1: Trying with individual xPath 
        d_xpath = '//div[@data-tab-content="details"]'

        

        details = driver.find_element_by_xpath(d_xpath).text
        print(details)

        i_xpath = '//div[@data-tab-content="ingredients"]'
        ingredients = driver.find_element_by_xpath(i_xpath).get_attribute("innerText")
        print(ingredients)

        # saves to CSV file 
        file_csv.writerow([product_name, product_subheading, rec_skintype, 
                           details, ingredients, item_link])

    unique_links = list_links[::4]

    for link in unique_links:
        print("\n", link)
        driver.get(link)
        time.sleep(3)
        product_content()
        driver.back()
    
# hover over skincare tab 
sc_tab = driver.find_element_by_xpath('//*[@id="node-1288"]/div/div/ul/li[2]/span')
ActionChains(driver).move_to_element(sc_tab).perform()

# LOOP - For ONLY CATEGORY, load page and scroll to bottom (lazyload
driver.find_element_by_xpath('//*[@id="node-9062"]/div/section/div[2]/div[1]/div/article/div/div/div/ul[1]')

links_var = driver.find_elements_by_xpath('//a[contains(@href, "/products/")]')
list_category = [link.get_attribute('href') for link in links_var]

for link in list_category:
    print("\n", link)
    driver.get(link)
    time.sleep(2)
    category_pages()
    driver.back()




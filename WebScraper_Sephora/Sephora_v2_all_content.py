import csv 
import time
import re
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

url= "https://www.sephora.com/search?keyword=skincare&pageSize=60&currentPage=61"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

file_csv = csv.writer(open('Sephora_{}.csv'.format(date.today()), 'w'))
file_csv.writerow(['Brand', 'Product', 'Ingredients', 'Item Link'])

wait = WebDriverWait(driver, 1) # 3

# closes Sephora sign-in pop up window
driver.find_element_by_class_name("css-1mfnet7").click() # "css-ll28en"
time.sleep(0.2) #3

def get_info():
    # scroll down to load dynamic content
    body_elem = driver.find_element_by_tag_name("body")
    no_of_pagedowns = 7

    while no_of_pagedowns:
        body_elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1

    list_links = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//a[contains(@href,'/product/')]")]

    for link in list_links:
        time.sleep(1) # 3
        print(link, "\n")
        driver.get(link)
        product_content()
        driver.back()

    # driver.find_element_by_class_name("css-1be47h1").click()

    next_button_exist() 

def product_content():
    soup = BeautifulSoup(driver.page_source, 'lxml') 
    soup.prettify()
    item_link = driver.current_url

    product_info = soup.find("div", {"class":"css-1svebj0"}) #css-19965sg
    brand = list(product_info.children)[0].next_element.next_element.text
    product = list(product_info.children)[0].next_element.next_sibling.text

    description = str(soup.find("div", {"class": "css-1pbcsc"})) #css-1vwy1pm 

    def remove_html_tags(text):
        # remove <br/>
        clean = re.compile('<br/>')
        new = re.sub(clean, '', text)
        #print(new, type(new))

        # remove bold tags and added commas
        no_front_b = new.replace("<b>", ",")
        no_end_b = no_front_b.replace("</b>", ",")
        #print(no_end_b, type(no_end_b))

        # remove all other HMTL tags
        clean = re.compile('<.*?>')
        no_html_tags = re.sub(clean, '', no_end_b) 
        #print(no_html_tags, type(no_html_tags))

        # replace returns with no space
        no_ws = no_html_tags.replace("\n", "")
        #print(no_ws, type(no_ws))

        split = no_ws.split(",")
    
        return split

    content = remove_html_tags(description)
    print(content)

    # Ingredients - finds ingredients tab and collects text from it, if present.
    ingredient_text_format = ""
    try: 
        if driver.find_element_by_xpath("//span[contains(string(), 'Ingredients')]//.."): 
            ingredient_div = driver.find_element_by_xpath("//span[contains(string(), 'Ingredients')]//..")
            driver.execute_script("arguments[0].click();", ingredient_div)
            ingredient_class = driver.find_element_by_xpath("(//*[@class='css-192qj50'])[3]") 
            ingredient_text = ingredient_class.text
            ingredient_text_format = ingredient_text.split("\n") 
    except NoSuchElementException:
        ingredient_text_format = ""

    # clean up: ingredients 
    if len(ingredient_text_format) > 1:
        ingredient_text_format = ",".join(ingredient_text_format)
    else:
        pass
    


    file_csv.writerow([brand, product, ingredient_text_format, item_link])
    print([brand, product, ingredient_text_format])
    
    time.sleep(0.5) #2

def next_button_exist():
    WebDriverWait(driver, 3) # 5
    
    next_button_xpath = "//*[name()='path' and @d='M57 142.5L9.5 95 0 104.5l38 38-38 38 9.5 9.5L57 142.5z']//..//../following-sibling::button[last()]"
    if driver.find_element_by_xpath(next_button_xpath).get_attribute("disabled"):
        print("Button disabled and this is the last page!")
        time.sleep(3)
        driver.quit()
        print("Sephora.csv file created")
    else: 
        print("Next button found")
        driver.find_element_by_xpath(next_button_xpath).click()
        time.sleep(0.1)
        get_info()

get_info()



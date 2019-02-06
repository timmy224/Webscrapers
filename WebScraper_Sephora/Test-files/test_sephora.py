import csv 
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# first page (TASK: need to iterate)
url = "https://www.sephora.com/search?keyword=skincare&pageSize=10&currentPage=1"

# opens up url in Google Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

# initiate excel spreadsheet
file_csv = csv.writer(open('Sephora.csv', 'w'))
file_csv.writerow(['Brand', 'Product', 'What it is', 'what is product used for' ,
                  'If you want to know more', 'Ingredients'])

wait = WebDriverWait(driver, 5)

# closes Sephora sign-in pop up window
driver.find_element_by_class_name("css-ll28en").click()
time.sleep(3)

def get_info():
    # scroll
    body_elem = driver.find_element_by_tag_name("body")
    no_of_pagedowns = 7

    while no_of_pagedowns:
        body_elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1

    list_links = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//a[contains(@href,'/product/')]")]

    for link in list_links:
        time.sleep(0.3)
        print(link, "\n")
        driver.get(link)
        # plug functions in here
        product_content()
        driver.back()
        next_button_exist()

    # driver.find_element_by_class_name("css-1be47h1").click()

    next_button_exist() 

"""
def brand_and_productName():
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml') 
    soup.prettify()

    # ii. get brand and product name
    product_info = soup.find("div", {"class":"css-19965sg"})
    brand = list(product_info.children)[0].next_element.next_element.text
    product = list(product_info.children)[0].next_element.next_sibling.text
    #print(brand, product)

    # iii. get product description
    ## what_it_is = soup.find("b", text = "What it is:")
    ## what_it_is_desc = what_it_is.next_sibling.next_sibling.next_sibling
    #print(what_it_is_desc)

    return brand, product

brand_and_productName()
"""


def product_content():
    # iv. what is product used for?
    soup = BeautifulSoup(driver.page_source, 'lxml') 
    soup.prettify()

    product_info = soup.find("div", {"class":"css-19965sg"})
    brand = list(product_info.children)[0].next_element.next_element.text
    product = list(product_info.children)[0].next_element.next_sibling.text
    #print(brand, product, "\n")

    description = str(soup.find("div", {"class": "css-1vwy1pm"}))

    def remove_html_tags(text):
        # remove <br/>
        clean = re.compile('<br/>')
        new = re.sub(clean, '', text)
        #print(new, type(new))

        # remove bold tags and added commas
        no_front_b = new.replace("<b>", ",")
        no_end_b = no_front_b.replace("</b>", ",")
        #print(no_end_b, type(no_end_b))

        clean = re.compile('<.*?>')
        no_html_tags = re.sub(clean, '', no_end_b) 
        #print(no_html_tags, type(no_html_tags))

        no_ws = no_html_tags.replace("\n", "")
        #print(no_ws, type(no_ws))

        split = no_ws.split(",")
        # remove first blank value
        # del split[0]
        return split
        #print(split, type(split))

    content = remove_html_tags(description)
    #print(content)

    def what_it_is(text):
        if "What it is:" in text:
            what_it_is_header = text.index("What it is:")
            print(text[what_it_is_header + 1])
            what_it_is_desc_2 = text[what_it_is_header + 1]
            return what_it_is_desc_2
        else:
            print("what it is not found")
    #print(content[content.index("what it is:")+1])

    what_it_is_desc = what_it_is(content)

    def solutions_for(text):
        if "Solutions for:" in text:
            solutions_for_header = text.index("Solutions for:")
            print(text[solutions_for_header + 1])
            solutions_desc = text[solutions_for_header + 1]
            return solutions_desc
        else:
            print("solutions for not found")
        
    solutions_desc = solutions_for(content)

    def if_you_want_to_know_more(text):
        if "If you want to know more…" in content:
            if_you_want_to_know_more_header = text.index("If you want to know more…")
            print(text[if_you_want_to_know_more_header + 1])
            if_you_want_to_know_more_desc = text[if_you_want_to_know_more_header + 1]
            return if_you_want_to_know_more_desc
        else:
            print("if you want to know more not found")
        
    if_you_want_to_know_more_desc = if_you_want_to_know_more(content)

    #vi. Ingredients
    ingredient_div = driver.find_element_by_xpath("//*[contains(text(), 'Ingredients')]//..")
    
    """
    def check_exists_by_xpath(xpath):
    try:
        webdriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
    """

    if driver.find_element_by_xpath("//*[contains(text(), 'Ingredients')]//..") == True:
        driver.execute_script("arguments[0].click();", ingredient_div)
        ingredient_class = driver.find_element_by_xpath("//*[@class='css-1kianer']//div[3]")
        ingredient_content = ingredient_class.text
        ingredient_text = ingredient_content.split("\n") 
    else:
        ingredient_text = ""
        
    
    

    #file_csv.writerow
    print([brand, product, what_it_is_desc, solutions_desc, if_you_want_to_know_more_desc, ingredient_text])
    time.sleep(10)
def next_button_exist():
    WebDriverWait(driver, 5)
    
    next_button_xpath = "//*[name()='path' and @d='M57 142.5L9.5 95 0 104.5l38 38-38 38 9.5 9.5L57 142.5z']//..//../following-sibling::button[last()]"
    if driver.find_element_by_xpath(next_button_xpath).get_attribute("disabled"):
        print("Button disabled and this is the last page!")
        time.sleep(3)
        driver.quit()
    else: 
        print("Next button found")
        driver.find_element_by_xpath(next_button_xpath).click()
        ## driver.find_element_by_class_name("css-xswd36").click()
        time.sleep(3)
        get_info()

get_info()



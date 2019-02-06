import csv 
import time
import re
from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

url= "https://www.sephora.com/search?keyword=clinique&pageSize=60&currentPage=1"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

file_csv = csv.writer(open('Sephora_Clinique_{}.csv'.format(date.today()), 'w'))
file_csv.writerow(['Brand', 'Product', 'What it is', 'what is product used for',
                   'If you want to know more', 'Ingredients', 'Item Link'])

wait = WebDriverWait(driver, 1) # 3

# closes Sephora sign-in pop up window
driver.find_element_by_class_name("css-1mfnet7").click() # "css-ll28en"
time.sleep(1) #3

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
        time.sleep(3) # 3
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
    
    # What it is: content
    what_it_is_desc_2 = []
    if "What it is:" in content and "Solutions for:" in content:
        what_it_is_header = content.index("What it is:")
        solutions_for_header = content.index("Solutions for:")
        for each in range(what_it_is_header + 1, solutions_for_header):
            what_it_is_desc_2.append(content[each])
            
    elif "What it is:" in content and "If you want to know more…" in content:
        what_it_is_header = content.index("What it is:")
        if_you_want_to_know_more_header = content.index("If you want to know more…")
        for each in range(what_it_is_header + 1, if_you_want_to_know_more_header):
            what_it_is_desc_2.append(content[each])

    elif "What it is:" in content and "What it is formulated to do:" in content:
        what_it_is_header = content.index("What it is:")
        what_its_formulated_header = content.index("What it is formulated to do:")
        for each in range(what_it_is_header + 1, what_its_formulated_header):
            what_it_is_desc_2.append(content[each])
    else:
        print("what it is not found")

    # Solutions for: content
    solutions_desc = []
    if "Solutions for:" in content:
        solutions_for_header = content.index("Solutions for:")
        if_you_want_to_know_more_header = content.index("If you want to know more…")
        for each in range(solutions_for_header + 1, if_you_want_to_know_more_header):
            solutions_desc.append(content[each])
    else:
        print("solutions for not found")
    
    # If you want to know more… content
    if_you_want_to_know_more_desc = []
    if "If you want to know more…" in content and "What it is formulated WITHOUT:" in content:
        if_you_want_to_know_more_header =  content.index("If you want to know more…")
        what_it_is_fomulated_without_header = content.index("What it is formulated WITHOUT:")
        for each in range(if_you_want_to_know_more_header + 1, what_it_is_fomulated_without_header):
            if_you_want_to_know_more_desc.append(content[each])
    elif "If you want to know more…" in content and "This set contains:" in content:
        if_you_want_to_know_more_header =  content.index("If you want to know more…")
        this_set_contains_header = content.index("This set contains:")
        for each in range(if_you_want_to_know_more_header + 1, this_set_contains_header):
            if_you_want_to_know_more_desc.append(content[each])
    else:
        print("if you want to know not found")

    # Ingredients - finds ingredients tab and collects text from it, if present.  
    ingredient_text_format = ""
    try: 
        if driver.find_element_by_xpath("//span[contains(string(), 'Ingredients')]//.."): 
            ingredient_div = driver.find_element_by_xpath("//span[contains(string(), 'Ingredients')]//..")
            driver.execute_script("arguments[0].click();", ingredient_div)
            ingredient_class = driver.find_element_by_xpath("(//*[@class='css-192qj50'])[3]") #css-1kianer # css-192qj50
            ingredient_text = ingredient_class.text
            ingredient_text_format = ingredient_text.split("\n") 
    except NoSuchElementException:
        ingredient_text_format = ""
   
    """
    # IN PROGRESS - working on for loop to replace existing clean up
    corrections = [what_it_is_desc_2, if_you_want_to_know_more_desc, ingredient_text]
    
    new = []
    j = ""
    for i in corrections:
        if (len(i)) > 1:
            for j in i:
                j = ''.join(j)

        else:
            for j in i:
                pass
        new.append(j)
    print(new)
    """
    
    ### WORKING
    # clean up: what it is
    if len(what_it_is_desc_2) > 1:
        what_it_is_desc_2 = "".join(what_it_is_desc_2)
    else:
        pass

    # clean up: if you want to know more 
    if len(if_you_want_to_know_more_desc) > 1:
        if_you_want_to_know_more_desc = "".join(if_you_want_to_know_more_desc)
    else:
        pass

    # clean up: ingredients 
    if len(ingredient_text_format) > 1:
        ingredient_text_format = ",".join(ingredient_text_format)
    else:
        pass
    
    """
    # clean up: if ["*string*"] format, remove [""]
    for i in content: 
        for j in i:
            string_checker = '[".*?"]'
            if j == string_checker:
                j.replace('["', "") # removes starting bracket and quotes
                j.replace('"]', "") # removes ending bracket and quotes 
    """


    file_csv.writerow([brand, product, what_it_is_desc_2, solutions_desc, if_you_want_to_know_more_desc, ingredient_text_format, item_link])
    print([brand, product, what_it_is_desc_2, solutions_desc, if_you_want_to_know_more_desc, ingredient_text_format])
    
    time.sleep(1) #2

def next_button_exist():
    WebDriverWait(driver, 3) # 5
    
    next_button_xpath = "//*[name()='path' and @d='M57 142.5L9.5 95 0 104.5l38 38-38 38 9.5 9.5L57 142.5z']//..//../following-sibling::button[last()]"
    if driver.find_element_by_xpath(next_button_xpath).get_attribute("disabled"):
        print("Button disabled and this is the last page!")
        time.sleep(5)
        driver.quit()
        print("Sephora.csv file created")
    else: 
        print("Next button found")
        driver.find_element_by_xpath(next_button_xpath).click()
        time.sleep(0.1)
        get_info()

get_info()



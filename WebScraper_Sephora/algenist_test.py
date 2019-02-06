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

url = "https://www.sephora.com/product/overnight-restorative-cream-P296415?icid2=products%20grid:p296415:product"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

def product_content():
    soup = BeautifulSoup(driver.page_source, 'lxml') 
    soup.prettify()

    # item_link = driver.current_url

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

        splitted = no_ws.split(",")

        # need to find string that contains "What it is:"
        

        return splitted

    content = remove_html_tags(description)
    
    for each in content:
            if "What it is:" in each: # finds string with "What it is:"
                # 1. CHECK - find index of string in list 
                # print(content.index(each))

                # 2. split the string 
                header_split = each.rpartition("What it is:")
                #print(header_split)

                # 3. delete index of old string
                content.pop(0)

                # 4. insert new strings back into list 
                single_header = header_split[1]
                double_header = header_split[1:3]
                combined = header_split[1] + " " + header_split[2]
                print(single_header, double_header, combined)

                #content.insert(0, single_header)
                #print(content)
                """
                for string in reversed(header_split):
                    # print(content.insert(0, string))
                    content.insert(0, string)
                    # print(content)
                """
                # need to return split string back into original string
                break
            else:
                print("not found")
                


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
        print("what it is not found", "\n")

    # Solutions for: content
    solutions_desc = []
    if "Solutions for:" in content:
        solutions_for_header = content.index("Solutions for:")
        if_you_want_to_know_more_header = content.index("If you want to know more…")
        for each in range(solutions_for_header + 1, if_you_want_to_know_more_header):
            solutions_desc.append(content[each])
    else:
        print("solutions for not found", "\n")
    
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
        print("if you want to know not found", "\n")

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

    # file_csv.writerow([brand, product, what_it_is_desc_2, solutions_desc, if_you_want_to_know_more_desc, ingredient_text_format, item_link])
    # print([brand, product, what_it_is_desc_2, solutions_desc, if_you_want_to_know_more_desc, ingredient_text_format])
    
    time.sleep(1) #2

product_content()
# get_info()
import csv 
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_info():
    # first page (TASK: need to iterate)
    url = "https://www.sephora.com/search?keyword=skincare&pageSize=300"

    # opens up url in Google Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)

    # closes Sephora sign-in pop up window
    popUp_close = driver.find_element_by_class_name("css-ll28en").click()
    time.sleep(0.2)

    # Single Item (need to iterate for all items)
    # Brand name: Dr. Dennis Gross Skincare: 
    # Product name: Alpha Beta® Extra Strength Daily Peel Mini
    product_click = driver.find_element_by_class_name("css-ktoumz").click()
    time.sleep(0.05)

    """ below should belong in get_info() """
    # creates CSV file to write
    file_csv = csv.writer(open('Sephora.csv', 'w'))
    file_csv.writerow(['Brand', 'Product', 'Details', 'How To Use', 'Ingredients'])

    soup = BeautifulSoup(driver.page_source, 'html5lib') 
    soup.prettify()

    # goes to div with brand and product name
    product_info = soup.find("div", {"class":"css-19965sg"})
    # gets brand name
    brand = list(product_info.children)[0].next_element.next_element.text
    # gets product name
    product = list(product_info.children)[0].next_element.next_sibling.text

    # gets product description
    what_it_is = soup.find("b", text = "What it is:")
    what_it_is_desc = what_it_is.next_sibling.next_sibling.next_sibling
    print(what_it_is_desc))    

    # product description stuff
    description = soup.find("div", {"class": "css-1vwy1pm"})
    print(description)

    # What it is: - DONE
    what_it_is = soup.find("b", text = "What it is:")
    what_it_is_desc = what_it_is.next_sibling.next_sibling.next_sibling
    #print(what_it_is_desc)

    
    # Solutions for: - WORKING
    """
    solutions_btag = soup.find("b", text = "Solutions for:")
    next_btag = solutions_btag.find_next_sibling("b")
    #print(next_btag)
    
    def loop_to_next_btag(text, firstElement):
        text += str(firstElement.getText())
        if (firstElement.next_sibling.next_sibling == next_btag):
            return text
        else:
            return loop_to_next_btag(text, firstElement.next_sibling.next_sibling)
    targetString = loop_to_next_btag('', solutions_btag)
    print(targetString)
    """


    # If you want to know more - DONE
    know_more = soup.find("b", text = "If you want to know more…")
    know_more_desc = know_more.next_sibling.next_sibling.next_sibling
    # print(know_more_desc)

    
    # Ingredients - WORKING
    """
    ingredient_class = driver.find_element_by_xpath("//*[@class='css-1kianer']")
    ingredient_children = ingredient_class.find_elements_by_xpath(".//*")
    
    print(ingredient_children.get_attribute('value'))
    """

    """
    ## button = driver.find_elements_by_xpath("//div[@class = 'css-1iyg0mf']")
    ingredient_div = driver.find_element_by_xpath("//*[contains(text(), 'Ingredients')]//..")
    driver.execute_script("arguments[0].click();", ingredient_div)
    time.sleep(3)

    ingredient_class = driver.find_element_by_xpath("//*[@class='css-1kianer']//div[@style]")
   

    # print(ingredient_div.get_attribute('innerHTML'))
    print(driver.execute_script("return arguments[0].innerHTML", ingredient_class))
    
    #stuff = driver.execute_script("return arguments[0].getAttribute('style')", ingredient_div)
    #return stuff.getText()

    # description = soup.find("div", {"style":"", "class": "css-1vwy1pm"}).getText()
    # print(description)
    

    # ingredients = soup.find("div", {"class": "css-1vwy1pm"})

    # ingredients_inner = soup.find("div", {"class": "css-1kianer"}).get_attribute("innerHTML")
    #print(ingredients_inner)
    #print(ingredients_inner.execute_script("return arguments[0].innerHTML", ingredients_inner))

    """


    


    """
    product_info = soup.find("div", {"class":"css-19965sg"})
    print(product_info)
    """


    

    # product_location = soup.find_element_by_class_name("css-at8tjb")
    # product = product_location.text
    

"""
# first page (TASK: need to iterate)
url = "https://www.sephora.com/search?keyword=skincare&pageSize=300"

# opens up url in Google Chrome
driver = webdriver.Chrome()
driver.get(url)

# closes Sephora sign-in pop up window
popUp_close = driver.find_element_by_class_name("css-ll28en").click()

# Single Item (need to iterate for all items)
# Brand name: Dr. Dennis Gross Skincare: 
# Product name: Alpha Beta® Extra Strength Daily Peel Mini
product_click = driver.find_element_by_class_name("css-ktoumz").click()
"""

get_info()



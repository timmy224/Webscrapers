import csv 
import time
import re
from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as EC

url= "https://www.ulta.com/skin-care-suncare?N=27fe&No=0&Nrpp=48"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

file_csv = csv.writer(open('Ulta_Suncare_{}.csv'.format(date.today()), 'w'))
file_csv.writerow(['Brand', 'Product', 'Ingredients', 'Image Link','Item Link'])

counter = 48 # needs to be multiples of 48 until 912 (non-inclusive for 864)

"""
check last page for counter max www.ulta.com/skin-care-suncare?N=27fe
"""

while counter < 1152:
    def get_info():
        # scroll down to load dynamic content
        body_elem = driver.find_element_by_tag_name("body")
        no_of_pagedowns = 9

        while no_of_pagedowns:
            body_elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pagedowns-=1
        

        list_links = [link.get_attribute('href') for link in driver.find_elements_by_class_name("product")]
        #print(list_links)

        for each_link in list_links:
            print("\n", each_link, "\n")
            driver.get(each_link)
            product_content()
            driver.back()
        
    def product_content():
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'lxml') 
        item_link = driver.current_url

        try: 
            #brand_class = soup.find("a", {"class":"Anchor ProductMainSection__brandAnchor"})
            brand_xpath = driver.find_element_by_xpath('.//span[@class="ProductMainSection__brandName"]//a[@class="Anchor ProductMainSection__brandAnchor"]')
            brand = brand_xpath.text

            #product_info_span = soup.find("span", {"ProductMainSection__productName"})
            product_info_xpath = driver.find_element_by_xpath('//span[@class="ProductMainSection__productName"]')
            product = product_info_xpath.text

            print(brand, product, "\n")

        except NoSuchElementException:
            print("No brand and product name found")
        
        try:
            ingredient_click = driver.find_element_by_class_name("ProductDetail__ingredients")
            driver.execute_script("arguments[0].click();", ingredient_click)
            
            ingredient_div = soup.findAll("div", {"class":"ProductDetail__productContent collapse"})

            ingredients = ingredient_div
            print("ingredients", len(ingredients), "\n")

            """
            water_options = [
                "Water", "Purified Water", "Aqua (Water)", "Water (Aqua)", 
                "Water / Aqua / Eau", 
            ]
            """

            try: 
                if len(ingredients) > 1:
                    split_ingredients = str(ingredients[1]).split(",")
                    print("split ingredients", len(split_ingredients), "\n")
                    
                    first_ingredient_dirty = split_ingredients[0]
                    first_ingredient_clean = first_ingredient_dirty.split(">")
                    first_ingredient = first_ingredient_clean[1]
                
                    last_ingredient_dirty = split_ingredients[len(split_ingredients)-1]
                    last_ingredient_clean = last_ingredient_dirty.split(".")
                    last_ingredient = last_ingredient_clean[0]

                    middle_ingredients = split_ingredients[1:len(split_ingredients)-1]
                    print("middle ingredients", len(middle_ingredients), "\n")

                    if middle_ingredients[0] == ' Eau)':
                        middle_ingredients[0] = 'Water/Aqua/Eau'
                        middle_ingredients.append(last_ingredient)
                        print(middle_ingredients)

                    else: 
                        middle_ingredients.insert(0, first_ingredient)
                        middle_ingredients.append(last_ingredient)
                        print(middle_ingredients)
                else: 
                    print(ingredients)
                    split_ingredients = str(ingredients).split(",")
                    first_ingredient_dirty = split_ingredients[0]
                    first_ingredient_clean = first_ingredient_dirty.split(">")
                    first_ingredient = first_ingredient_clean[1]
                
                    last_ingredient_dirty = split_ingredients[len(split_ingredients)-1]
                    last_ingredient_clean = last_ingredient_dirty.split(".")
                    last_ingredient = last_ingredient_clean[0]

                    middle_ingredients = split_ingredients[1:len(split_ingredients)-1]

                    if middle_ingredients[0] == ' Eau)':
                        middle_ingredients[0] = 'Water/Aqua/Eau'
                        middle_ingredients.append(last_ingredient)
                        print(middle_ingredients)
                    else: 
                        middle_ingredients.insert(0, first_ingredient)
                        middle_ingredients.append(last_ingredient)
                        print(middle_ingredients)
            except IndexError:
                    # print this - middle_ingredients = "Check manually"
                try: 
                    if len(ingredients) > 1:
                        split_ingredients = str(ingredients[0]).split(",") # changed ingredients[1] to ingredients[0]
                        print("split ingredients", len(split_ingredients), "\n", split_ingredients, "\n")
                        
                        first_ingredient_dirty = split_ingredients[0]
                        first_ingredient_clean = first_ingredient_dirty.split(">")
                        first_ingredient = first_ingredient_clean[1]
                    
                        last_ingredient_dirty = split_ingredients[len(split_ingredients)-1]
                        last_ingredient_clean = last_ingredient_dirty.split(".")
                        last_ingredient = last_ingredient_clean[0]

                        middle_ingredients = split_ingredients[0:len(split_ingredients)-1]
                        print("middle ingredients", len(middle_ingredients), "\n",  middle_ingredients, "\n" * 2)

                        if middle_ingredients[0] == ' Eau)':
                            middle_ingredients[0] = 'Water/Aqua/Eau'
                            middle_ingredients.append(last_ingredient)
                            print(middle_ingredients)
                        else: 
                            middle_ingredients.insert(0, first_ingredient)
                            middle_ingredients.append(last_ingredient)
                            print(middle_ingredients)
                    else: 
                        print(ingredients)
                        split_ingredients = str(ingredients).split(",")
                        first_ingredient_dirty = split_ingredients[0]
                        first_ingredient_clean = first_ingredient_dirty.split(">")
                        first_ingredient = first_ingredient_clean[1]
                    
                        last_ingredient_dirty = split_ingredients[len(split_ingredients)-1]
                        last_ingredient_clean = last_ingredient_dirty.split(".")
                        last_ingredient = last_ingredient_clean[0]

                        middle_ingredients = split_ingredients[0:len(split_ingredients)-1]

                        if middle_ingredients[0] == ' Eau)':
                            middle_ingredients[0] = 'Water/Aqua/Eau'
                            middle_ingredients.append(last_ingredient)
                            print(middle_ingredients)
                        else: 
                            middle_ingredients.insert(0, first_ingredient)
                            middle_ingredients.append(last_ingredient)
                            print(middle_ingredients)
                            
                except IndexError:
                    middle_ingredients = "CHECK MANUALLY"
        except NoSuchElementException:
            middle_ingredients = ''
            print("Ingredients not found!")

        test_string = ''.join(middle_ingredients)
        test_string.strip('[')
        test_string.strip(']')

        time.sleep(5)
        try:   
            image_xpath = '//div[@class="s7staticimage"]//img'
            image_link = driver.find_element_by_xpath(image_xpath).get_attribute('src')
        except NoSuchElementException:
            image_link = 'Check Manually'

        try:
            print(brand, product, test_string, image_link)
            file_csv.writerow([brand, product, test_string, image_link, item_link])
        except UnboundLocalError:
            pass

    def next_page():
        global counter
        url = "https://www.ulta.com/skin-care-suncare?N=27fe&No={}&Nrpp=48".format(counter)
        driver.get(url)
        counter += 48
        time.sleep(3)
    get_info()
    next_page()



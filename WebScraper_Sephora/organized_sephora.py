import csv 
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#### 1. access Sephora page

# initial result page 
    url = "https://www.sephora.com/search?keyword=skincare&pageSize=300"

    # opens up url in Google Chrome (incognito)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)

    # closes Sephora sign-in pop up window
    popUp_close = driver.find_element_by_class_name("css-ll28en").click()
    time.sleep(0.05)

    # initiate excel spreadsheet
    file_csv = csv.writer(open('Sephora.csv', 'w'))
    file_csv.writerow(['Brand', 'Product', 'What it is', 'what is product used for' ,
                        'If you want to know more', 'Ingredients'])
    # variables: brand, product, what_it_is_desc, solution_content_final, know_more_desc, ind_ingredient_text

#### 2. create for loop that goes through each item on results page
    """ Need to Do """

    # a. for loop that clicks through each item on list
        """ clicks through single product atm"""
        product_click = driver.find_element_by_class_name("css-ktoumz").click()
        time.sleep(0.1)

        # i. gets source for each item
        soup = BeautifulSoup(driver.page_source, 'lxml') 
        soup.prettify()

        # ii. get brand and product name
        product_info = soup.find("div", {"class":"css-19965sg"})
        brand = list(product_info.children)[0].next_element.next_element.text
        product = list(product_info.children)[0].next_element.next_sibling.text
        print(brand, product)

        # iii. get product description
        what_it_is = soup.find("b", text = "What it is:")
        what_it_is_desc = what_it_is.next_sibling.next_sibling.next_sibling
        print(what_it_is_desc)

        # iv. what is product used for?
        description = soup.find("div", {"class": "css-1vwy1pm"})

        def remove_html_tags(text):
        """Remove html tags from a string"""
            import re
            clean = re.compile('<.*?>')
            return re.sub(clean, '', text)

        no_br = remove_html_tags(str(description))
        ind_lines = no_br.split("\n")
        
        start = ind_lines.index("Solutions for:")
        end = ind_lines.index("If you want to know more…")

        solutions_content = ind_lines[start+1:end]
        ran_out_of_names = list(map(str, solutions_content))
        solution_content_final = " ".join(ran_out_of_names)
        print(solution_content_final)

        # v. If you want to know more about product
        know_more = soup.find("b", text = "If you want to know more…")
        know_more_desc = know_more.next_sibling.next_sibling.next_sibling
        print(know_more_desc)

        #vi. Ingredients
        ingredient_div = driver.find_element_by_xpath("//*[contains(text(), 'Ingredients')]//..")
        driver.execute_script("arguments[0].click();", ingredient_div)

        ingredient_class = driver.find_element_by_xpath("//*[@class='css-1kianer']//div[3]")
        
        ingredient_text = ingredient_class.text
        ind_ingredient_text = ingredient_text.split("\n") 
        print(ind_ingredient_text)

#### 3. create for loop that goes through all the pages 
    """ To Do """
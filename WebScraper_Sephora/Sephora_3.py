import csv 
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# initial result page 
url = "hhttps://www.sephora.com/search?keyword=skincare&currentPage=59"

# opens up url in Google Chrome (incognito)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

def access_page():
    # closes Sephora sign-in pop up window
    driver.find_element_by_class_name("css-ll28en").click()
    time.sleep(0.05)

def excel_start():
    # initiate excel spreadsheet
    file_csv = csv.writer(open('Sephora.csv', 'w'))
    file_csv.writerow(['Brand', 'Product', 'What it is', 'what is product used for' ,
                        'If you want to know more', 'Ingredients'])
    # variables: brand, product, what_it_is_desc, solution_content_final, know_more_desc, ind_ingredient_text
    """ Need to link """

def results_page():
    # simulates scrolling through page to trigger dynamic content loading
    body_elem = driver.find_element_by_tag_name("body")

    pagedown_count = 7

    while pagedown_count:
        body_elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        pagedown_count -= 1

    # finds links for each item on results page
    driver.implicitly_wait(3)
    list_links = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//a[contains(@href,'/product/')]")]

    for link in list_links:
        print(link)
        driver.get(link)
        driver.back()
        # append to list for item info extract

def item_info():
     # i. gets page_source for item
    soup = BeautifulSoup(driver.page_source, 'lxml') 
    soup.prettify()

    # ii. get brand and product name
    product_info = soup.find("div", {"class":"css-19965sg"})
    brand = list(product_info.children)[0].next_element.next_element.text
    product = list(product_info.children)[0].next_element.next_sibling.text
    print(brand, product)
    # remove print and set to variable for csv write

    # iii. get product description
    what_it_is = soup.find("b", text = "What it is:")
    what_it_is_desc = what_it_is.next_sibling.next_sibling.next_sibling
    print(what_it_is_desc)
    # remove print and set to variable for csv write

    # iv. what is product used for?
    description = soup.find("div", {"class": "css-1vwy1pm"})

    def remove_html_tags(text):
        # Remove html tags from a string
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    # turns <br/> HTML tag into strings and replaces with \n
    no_br = remove_html_tags(str(description))
    ind_lines = no_br.split("\n")
    
    # set index of start and stop 
    start = ind_lines.index("Solutions for:")
    end = ind_lines.index("If you want to know more…")

    # extracts info and groups them together
    solutions_content = ind_lines[start+1:end]
    solutions_content_list = list(map(str, solutions_content))
    solution_content_final = " ".join(solutions_content_list )
    print(solution_content_final)
    # remove print and set to variable for csv write


    # v. If you want to know more about product
    know_more = soup.find("b", text = "If you want to know more…")
    know_more_desc = know_more.next_sibling.next_sibling.next_sibling
    print(know_more_desc)
    # remove print and set to variable for csv write

    #vi. Ingredients
    # finds container location for ingredients tab and points to parent
    ingredient_div = driver.find_element_by_xpath("//*[contains(text(), 'Ingredients')]//..")
    # JS script to turn display hidden ingredients text content
    driver.execute_script("arguments[0].click();", ingredient_div)

    # finds ingredient text location
    ingredient_class = driver.find_element_by_xpath("//*[@class='css-1kianer']//div[3]")
    
    # gets ingredients text and splits with whitespace
    ingredient = ingredient_class.text
    ingredient_text = ingredient.split("\n") 
    print(ingredient_text)
    # remove print and set to variable for csv write

#### 3. create for loop that goes through all the pages 
    """ To Do """
def next_page():
    next_button = driver.find_element_by_class_name("css-1be47h1")
    if not next_button:
        print("This is the last page!")  
    else: 
        driver.find_element_by_class_name("css-1be47h1").click()
import csv 
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# first page (TASK: need to iterate)
url = "https://www.sephora.com/search?keyword=skincare&pageSize=10&currentPage=1"

# opens up url in Google Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

# soup = BeautifulSoup(driver.page_source, 'html5lib') 
# soup.prettify()

# initiate excel spreadsheet
file_csv = csv.writer(open('Sephora.csv', 'w'))
file_csv.writerow(['Brand', 'Product', 'What it is', 'what is product used for' ,
                  'If you want to know more', 'Ingredients'])

wait = WebDriverWait(driver, 5)

# closes Sephora sign-in pop up window
driver.find_element_by_class_name("css-ll28en").click()
time.sleep(3)

def get_info():
    # soup = BeautifulSoup(driver.page_source, 'lxml') 
    # soup.prettify()

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
        print(link)
        driver.get(link)
        ind_prod_info()
        driver.back()

    # driver.find_element_by_class_name("css-1be47h1").click()

    next_button_exist() 

def ind_prod_info():
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html5lib') 
    soup.prettify()

    # ii. get brand and product name
    product_info = soup.find("div", {"class":"css-19965sg"})
    brand = list(product_info.children)[0].next_element.next_element.text
    product = list(product_info.children)[0].next_element.next_sibling.text
    #print(brand, product)

    # iii. get product description
    what_it_is = soup.find("b", text = "What it is:")
    what_it_is_desc = what_it_is.next_sibling.next_sibling.next_sibling
    #print(what_it_is_desc)

    # iv. what is product used for?
    description = soup.find("div", {"class": "css-1vwy1pm"})
    print(description)

    #Remove html tags from a string
    def remove_html_tags(text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text) 

    no_html = remove_html_tags(str(description))
    no_spec = re.sub(r"[\…, \:, \?]", ' ', no_html)
    ind_lines = no_spec.split("\n")

    print(no_spec, "\n", type(no_spec))
    print("\n")
    print(ind_lines, "\n", type(ind_lines))
    # insert if-else statement that checks whether ind_lines is a list of multiple index (what we want)
    # or if its a list of one (not what we want)
    if len(ind_lines) > 1: 
        pass
    else: 
        pass

    start = ind_lines.index("Solutions for ") #:
    end = ind_lines.index("If you want to know more ") #…

    solutions_content = ind_lines[start+1:end]
    ran_out_of_names = list(map(str, solutions_content))
    solution_content_final = " ".join(ran_out_of_names)
    #print(solution_content_final)

    # v. If you want to know more about product
    know_more = soup.find("b", text = "If you want to know more…")
    know_more_desc = know_more.next_sibling.next_sibling.next_sibling
    #print(know_more_desc)

    #vi. Ingredients
    ingredient_div = driver.find_element_by_xpath("//*[contains(text(), 'Ingredients')]//..")
    driver.execute_script("arguments[0].click();", ingredient_div)

    ingredient_class = driver.find_element_by_xpath("//*[@class='css-1kianer']//div[3]")
    
    ingredient_text = ingredient_class.text
    ind_ingredient_text = ingredient_text.split("\n") 
    #print(ind_ingredient_text)

    file_csv.writerow([brand, product, what_it_is_desc, solution_content_final, know_more_desc, ind_ingredient_text])

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



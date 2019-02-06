# To Do - need to account for searches that yield inappropriate results 
# (not restaurants)
import csv
import time
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def intro_file_prompt(): # CSV file location and file name confirmation
    prompt = "> "

    file_location_check = 'Please make sure CSV file is in current working' \
                          'directory.'
    print(file_location_check)

    file_name_check = "What is the name of the CSV file?"
    print(file_name_check)

    global file_name
    file_name = input(prompt)

    second_check = "Is this file name correct? {}".format(file_name)
    yn_message = "Please type yes or no to confirm."
    print(second_check)
    print(yn_message)

    confirmation = input(prompt)

    if confirmation == "yes":
        pass
    else:
        intro_file_prompt()

def driver_init():
    yelp_url = "https://www.yelp.com/"

    # chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    global driver
    driver = webdriver.Chrome(chrome_options = chrome_options)
    driver.get(yelp_url)

def CSV_file_stuff(): # read CSV file with restaurant names
    with open('{}'.format(file_name), encoding = 'ISO-8859-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader) # skip header row
        line_count = 0
        global restaurant_list
        restaurant_list = []
        for row in csv_reader:
            restaurant_list.append(row[0]) # 0 designates first column
            line_count += 1 

    # create new CSV file 
    global file_csv
    file_csv = csv.writer(open('Yelp-Scraper_{}.csv'.format(date.today()), 'w'))
    file_csv.writerow(['Name', 'Cuisine', 'Budget', 'Neighborhood', \
                    'Street Address','Menu/Special', 'Notes', 'Yelp Link'])

def enter_restaurant_name(name): # enter restaurant name 
    search_box = driver.find_element_by_id('find_desc')
    search_box.send_keys(name)
    
    location_box = driver.find_element_by_id('dropperText_Mast')
    location_box.clear()
    location_box.send_keys('New York, NY')
    
    search_btn = driver.find_element_by_id('header-search-submit')
    search_btn.click()

    driver.implicitly_wait(1) # seconds
    
    #first_result_class = 'biz-name js-analytics-click'

    try:
        first_result_xpath = '(//span[@class="indexed-biz-name"])[1]/a'
        results = driver.find_element_by_xpath(first_result_xpath)
        restaurant_link = results.get_attribute('href')
        driver.get(restaurant_link)
    except NoSuchElementException:
        first_result_xpath = '(//h3[@class="lemon--h3__373c0__5Q5tF ' \
                              'heading--h3__373c0__1n4Of ' \
                              'alternate__373c0__1uacp" ' \
                              'and contains(text(), "1")])[1]/a'
        #class="lemon--h3__373c0__5Q5tF heading--h3__373c0__1n4Of alternate__373c0__1uacp"
        results = driver.find_element_by_xpath(first_result_xpath)
        restaurant_link = results.get_attribute('href')
        driver.get(restaurant_link)

def get_restaurant_info():
    yelp_link = driver.current_url
    name_elem = driver.find_element_by_class_name('biz-page-title')
    name = name_elem.text

    cuisine_elem = driver.find_element_by_xpath('(//span[@class='\
                                                '"category-str-list"])[1]')
    cuisine = cuisine_elem.text

    budget_xpath = '(//span[@class="business-attribute price-range"])[1]'
    budget_elem = driver.find_element_by_xpath(budget_xpath)
    budget = budget_elem.text

    street_address_xpath= '//strong[@class="street-address"]'
    street_address_elem = driver.find_element_by_xpath(street_address_xpath)
    street_address = street_address_elem.text

    neighborhood_xpath = '//span[@class="neighborhood-str-list"]'
    neighborhood_elem = driver.find_element_by_xpath(neighborhood_xpath)
    neighborhood = neighborhood_elem.text
    
    print(name, cuisine, budget, "\n", street_address, "\n", neighborhood, "\n")
    file_csv.writerow([name, cuisine, budget, '', '', '', '', yelp_link])

intro_file_prompt()
driver_init()
CSV_file_stuff()

for restaurant in restaurant_list:
    enter_restaurant_name(restaurant)
    get_restaurant_info()
    for _ in range(2):
        driver.back()

time.sleep(10)
print("Output file created:", 'Yelp-Scraper_{}.csv'.format(date.today()))
driver.quit()


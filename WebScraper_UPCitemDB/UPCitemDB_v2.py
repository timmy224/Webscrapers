import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_info():
    # creates CSV file to write UPC and Product name into
    file_csv = csv.writer(open('UPCitemDB_{}.csv'.format(brand), 'w'))
    file_csv.writerow(['UPC', 'Product Name'])

    # Beautifulsoup module parses document and extraction
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup.prettify()

    # finds all HTML class = 'rImage" tags (UPC and Product Name nested in here)
    for stuff in soup.find_all(class_="rImage"):
        important_text = stuff.get_text()
        UPC = important_text[:12]
        Product_name = important_text[12:]

        # writes to CSV file; see line 25 to 27
        file_csv.writerow([UPC, Product_name])


try: 
    url = "https://www.upcitemdb.com/"
    print("What is the brand name?")
    brand = input("> ")

    # opens up UPCitemDB.com in Chrome
    driver = webdriver.Chrome()
    driver.get(url)

    # enters brand into search bar and returns search results
    search_entry = driver.find_element_by_name('s')
    search_entry.clear()
    search_entry.send_keys(brand)
    search_entry.send_keys(Keys.RETURN)

    assert "We could not find any UPC numbers associated with the product name" not in driver.page_source

    get_info()
    driver.close()
    print("File created: UPCitemDB_{}.csv".format(brand))

except:
    driver.close()
    print("Brand not found!")

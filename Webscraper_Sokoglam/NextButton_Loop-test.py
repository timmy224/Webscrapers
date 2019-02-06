import time 
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
#chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1440x900')

driver = webdriver.Chrome(options=chrome_options)


url = 'https://sokoglam.com/collections/skincare?page=1'

driver.get(url)

time.sleep(5)

def checkNextButton():

    global next_button_status
    next_button_status = True

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    
    try: 
        close_PopUp = driver.find_element_by_xpath('//a[@title = "Close"]')
        close_PopUp.click()

        time.sleep(3)
    
    except NoSuchElementException:
        print('No Pop-Up detected')
        pass

    try:
        next_button = driver.find_element_by_xpath('//a[. = "Next »" ]')
        next_button.click()

    except NoSuchElementException:
        print('--- Last page! ---')
        next_button_status = False
        return next_button_status
        
with open('random.csv', 'w') as f:
    file_csv = csv.writer(f)
    file_csv.writerow(['Test1', 'Test2'])

    while True:

        checkNextButton()
        count = 'works'

        if next_button_status == False: 
            break
            
        else:
            print('Break didn\'t work') 
            print(count)
            file_csv.writerow([count, 'Empty'])
    
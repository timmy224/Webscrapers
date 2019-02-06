import csv
import time
from selenium import webdriver

# chrome settings
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options=chrome_options)

# create CSV files
file_csv = csv.writer(open('IE_Project-Mexico_TempData.csv', 'w'))
file_csv.writerow(['Month', 'Year', 'Temperature(Fahrenheit)'])

years = list(range(2008, 2019))

months = [1, 2, 3, 10, 11, 12] 

for each_year in years:
    for each_month in months:

        # access webpage for Oct-March months for years 2008 - 2018
        url = 'https://www.wunderground.com/history/monthly/mx/mexico-city-airport/MMMX/date/{}-{}'.format(each_year, each_month)
        driver.get(url)
        time.sleep(3)

        average_temp_xpath = driver.find_element_by_xpath("//th[contains(text(),'Avg Temperature')]//following-sibling::td[2]")
        average_temp = average_temp_xpath.text

        month = each_month
        year = each_year
        temperature = average_temp

        file_csv.writerow([month, year, temperature])
        print(month, year, temperature)







        

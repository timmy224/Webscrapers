# WebScraper Tutorial - https://www.datacamp.com/community/tutorials/web-scraping-using-python
# 1. extract data from web - lines 11 to 122
# 2. clean data using Pandas library - lines 124 to 185
# 3. visualize data using Matplotlib library - lines 187 to 251

# Deviations from Tutorial
# Will be using REQUEST libraries instead of urllib.request
# Will not be renaming library imports to help become familiar with library function

# provides fast, flexible, and expressive data structures
import pandas
# for scientific computing
import numpy
# 2D plotting library 
import matplotlib.pyplot as pyplot
# statistical data visualization
import seaborn 

# requests library allows for interaction with websites and opening HTTP URLs.
import requests

"""from urllib.request import urlopen"""
from bs4 import BeautifulSoup

"""
# see link: https://stackoverflow.com/questions/31290445/need-to-find-the-requests-equivalent-of-openurl-from-urllib2
The equivalent of urllib method
1. urlopen("website_link_here") - output is response that is read

IS

2.  requests.get("website_link_here").text - which has a .text method added to end
"""

# URLLIB method 
"""
#url = "http://www.hubertiming.com/results/2017GPTR10K"
#html = urlopen(url)
#print(html)
#soup = BeautifulSoup(html, 'lxml')
"""

# REQUESTS method
# gets from following URL and doesn't need to verify SSL certificate
# see .text method added to end of line 42!
r = requests.get("http://www.hubertiming.com/results/2017GPTR10K").text
# lxml processes xml and html
soup = BeautifulSoup(r, 'lxml') 

""" 
--- Finding specific elements and all text --- 
# prints all text 
text = soup.get_text()

# prints title of webpage; html tag <title>
title = soup.title 

# prints all <a> elements
a_elements = soup.find_all('a')
print(elements)
# finds only hyperlinks from anchor tags
for link in a_elements:
    print(link.get("href"))

# 'table' argument for <table> tags

# 'tr' argument for <tr> table row tags
rows = soup.find_all('tr')
    # gets rows from the very first to the 9th row. 10th row not inclusive
print(rows[:10])

# 'th' argument for <th> table header tags

# 'td' argument for <td> table cell tags

"""
# BeautifulSoup: finds all elements in table row <tr> html tags
rows = soup.find_all('tr')
    # gets rows from the very first to the 9th row. 10th row not inclusive
    # print(rows[:10])

# takes table from webpage and converts to dataframe for easier manipulation
# 1. Convert table rows into list form 
# 2. Convert list to dataframe

# for loop that goes over each table row and prints out each table cell
for row in rows: 
    row_td = row.find_all('td')
    # turns row_td into a string because row_td datatype is resultSet
    str_cells = str(row_td)


# BeautifulSoup: extract text without html tags
cleantext = BeautifulSoup(str_cells, 'lxml').get_text()
list_rows = []
for row in rows:
    row_td = row.find_all('td')
    str_cells = str(row_td)
    cleantext = BeautifulSoup(str_cells, 'lxml').get_text()
    list_rows.append(cleantext)
"""

# generates an empty list, extract text from html tags for each row, and append it to the assigned list
import re

list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    # lines 107 and 109 - regex that that replaces characters found in <td> tags with empty string for each table row. 
    # re.compile() method - compile regex by passing string to match
    # '<.#?>' finds shortest possible string, '<.*>' matches all text between opening and closing brackets
    clean = re.compile('<.*?>')
    # re.sub() method - finds substring where regex matches and replaces with empty string
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)
"""

# Pandas: convert list into dataframe
df = pandas.DataFrame(list_rows)
# Pandas: df.head() returns first n rows
# print(df.head(10))

# Pandas: split "0" column using "," as separator 
# Pandas.str.split(): expand = True, return DataFrame/MultiIndex expanding dimensionality.
# Pandas.str.split(): expand = False, return Series/Index, containing lists of strings.
df1 = df[0].str.split(',', expand = True)

# Pandas.str.strip() removes unwanted characters (just opening brackets from column 0)
df1[0] = df1[0].str.strip('[')

# BeautifulSoup: finds missing table headers from <th> tags in webpage
col_labels = soup.find_all('th')

# creates empty list, turns col_labels into string
all_header = []
col_str = str(col_labels)
# BeautifulSoup: col_str gets passed into BeautifulSoup and extracts text
cleantext_header = BeautifulSoup(col_str, 'lxml').get_text()
all_header.append(cleantext_header)

# convert into Pandas dataframe
df2 = pandas.DataFrame(all_header)
# print(df2.head())

# split all_headers column using ',' as separator
df3 = df2[0].str.split(',', expand = True)
# print(df3.head())

# all_header dataframe and cleantext dataframe can be concatenated together
# array set in the order of combined table
frames = [df3, df1]

# new dataframe is concatenated from frames variable
df4 = pandas.concat(frames)
# print(df4.head())

# assigns first row as column header
# dataframe.iloc - integer based indexing; df4 column is renamed using df4's first row of values (in this case: string)
df5 = df4.rename(columns = df4.iloc[0])
# print(df5.head())

# displays information of dataframe 
df5.info()
# displays tuple regarding dataframe dimension 
df5.shape

# drop rows with missing values
# axis = 0: drops rows; axis = 1: drops columns
# how = 'any': if any NA values are present, drop that row/column; how = 'all': if all values are NA, drop row/column
df6 = df5.dropna(axis = 0, how = 'any')
# print(df6.head())

# drop replicated table header on row 0
df7 = df6.drop(df6.index[0])
# print(df7.head())

# clean column names 
df7.rename(columns = {'[Place': 'Place'}, inplace = True)
df7.rename(columns = {' Team]': 'Team'}, inplace = True)
# print(df7.head())

# remove closing brackets in cells under the "Team" column
df7['Team'] = df7['Team'].str.strip(']')
# print(df7.head())
"""
Question 1: What was the average time for the runners?
""" 
# Take cells under appropriate column and turn into list
time_list = df7[' Chip Time'].tolist()

time_mins = []
for i in time_list:
    h, m, s = i.split(":")
    math = (int(h) * 3600 + int(m) * 60 + int(s)) / 60
    time_mins.append(math)

# print(time_mins)

# convert time_mins list to dataframe and add under new column "Runner_mins"
df7["Runner_mins"] = time_mins
# print(df7.head())

# Pandas: dataframe.describe() generates descriptive statistics that summarize central tendency, dispersion, and shape of dataset distribution
# NumPy.number is used to limit descriptive statistics that are only numerical - count, mean, max, min, std, quartiles
df7.describe(include = [numpy.number])

# Boxplot visualization
pyplot.figure(1)

pyplot.rcParams['figure.figsize'] = 15, 5

df7.boxplot(column = 'Runner_mins')
pyplot.grid(True, axis = 'y')
pyplot.ylabel('Chip Time')
pyplot.xticks([1], ['Runners'])
pyplot.show()
# pyplot.close() # used for multiple graphs

"""
Question 2: Did the runner's finish times follow a normal distribution?
"""
pyplot.figure(2)
x = df7['Runner_mins']
ax = seaborn.distplot(x, hist = True, kde = True, color = 'm', rug = False, bins = 25, hist_kws={'edgecolor': 'black'})
pyplot.show()
# pyplot.close() # used for multiple graphs

"""
Question 3: Were there any performances between males and females of various age groups?
"""
pyplot.figure(3)
f_fuko = df7.loc[df7[' Gender'] == ' F']['Runner_mins']
m_fuko = df7.loc[df7[' Gender'] == ' M']['Runner_mins']
seaborn.distplot(f_fuko, hist = True, kde = True, rug = False, hist_kws = {'edgecolor': 'black'}, label = 'Female')
seaborn.distplot(m_fuko, hist = True, kde = True, rug = False, hist_kws = {'edgecolor': 'black'}, label = 'Male')
pyplot.legend()
pyplot.show()
# pyplot.close()

# Descriptive statistics for each gender group
group_stats = df7.groupby(" Gender", as_index = True).describe()
print(group_stats)

# side-by-side boxplot comparision between gender groups
pyplot.figure(4)
df7.boxplot(column = "Runner_mins", by = " Gender")
pyplot.ylabel("Chip Time")
pyplot.suptitle("")

pyplot.show()
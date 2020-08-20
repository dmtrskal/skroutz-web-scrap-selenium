# install Python3 (https://datascience.com.co/how-to-install-python-2-7-and-3-6-in-windows-10-add-python-path-281e7eae62a)
# download geckodriver (https://github.com/mozilla/geckodriver/releases)

# pip install xlrd
# pip install selenium
# pip install progressbar2

import os
import sys
import xlrd
import re
import csv
import datetime
import time
from progressbar import progressbar

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


scroll_pause_time = 0.5
page_offset = 300


datetime_object = datetime.datetime.now()
timestampStr = datetime_object.strftime("%d-%b-%Y_%H-%M-%S")
#print('Current Timestamp : ', timestampStr)

out_filename = "skroutz-shops" + "__" + timestampStr + ".csv"


# Read input file and create the input lists
if len(sys.argv) < 2:
    print("Please give an excel file as argument!!")
    sys.exit()

wb = xlrd.open_workbook(sys.argv[1])
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

quote_page_list = []
price_limit_list = []
no_url_products_list = []
for i in range(1, sheet.nrows):
    # only Products with URL are searched
    if not str(sheet.cell_value(i, 2)):
        no_url_products_list.append(str(sheet.cell_value(i, 0)))
    else:
        quote_page_list.append(str(sheet.cell_value(i, 2)))
        price_limit_list.append(sheet.cell_value(i, 1))


if len(no_url_products_list) != 0:
    print(30 * "*")
    print("Products without URL = " + str(no_url_products_list) + "\n")
    print(30 * "*")

# Read HTML page and create output file
try:
    with open(out_filename, 'w', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        for page, price_limit,i in zip(quote_page_list, price_limit_list, progressbar(range(len(quote_page_list)))):
            # Establish connection and get page
            driver = webdriver.Firefox(executable_path=os.path.join(
                os.path.abspath(os.getcwd()), "geckodriver.exe"))
            driver.get(page)

            #page_height = driver.execute_script("return document.body.scrollHeight;")
            #print("Page height is: " + str(page_height))

            scroll_by_script = "scrollBy(0,{})".format(page_offset)

            pos = driver.execute_script("return window.pageYOffset;")
            last_height = pos
            while True:
                driver.execute_script(scroll_by_script)

                pos = driver.execute_script("return window.pageYOffset;")
                time.sleep(scroll_pause_time)

                #pos = driver.execute_script("return window.pageYOffset;")
                #print("Position is: " + str(pos))

                new_height = pos
                if new_height == last_height:
                    break
                last_height = new_height

            #print("LAST Position is: " + str(driver.execute_script("return window.pageYOffset;")))

            # Save HTML page in file
            # with open('page.html', 'w', encoding="utf-8") as f:
            #    f.write(driver.page_source)

            name_element_list = driver.find_elements_by_css_selector(
                    "div.shop-name")
            price_element_list = driver.find_elements_by_css_selector(
                    "div.price-content")
            # price_element_list = driver.find_elements_by_xpath("//div[@class='price-content']")   # same as above
            nested_price_element_list = driver.find_elements_by_xpath(
                    "//a[contains(@data-type,'net_price')]")

            #print(len(name_element_list))
            # print(name_element_list)

            # for t_name in name_element_list:
            #    print(t_name.text)

            #print(len(price_element_list))
            # print(price_element_list)
            # for t_price in price_element_list:
            #    print(t_price.text)

            #print(len(nested_price_element_list))
			
			
            title_element = driver.find_elements_by_css_selector(
                    ".page-title")
            title=title_element[0].text
            title = title.strip() # strip() is used to remove starting and trailing

            writer.writerow([title, price_limit])

            for name_element, nested_price_element in zip(name_element_list, nested_price_element_list):
                # Parse Name
                name = name_element.text.strip()  # strip() is used to remove starting and trailing
                #print(name)

                # Parse Price
                # strip() is used to remove starting and trailing
                price = nested_price_element.text.strip()
                #print(price)

                price = price.replace(".", "")  # fix prices >= 1000
                # Price with , as floating point
                str_price = re.findall("\d+\,\d+", price)
                str_price = str_price[0]

                # Price with . as floating point
                floatstr_price = str_price.replace(",", ".")
                #print(floatstr_price)

                # Parse Url
                url = nested_price_element.get_attribute("href")
                #print(url)

                # Perform price check and print to excel file only info with
                # prices BELOW Price limit variable
                if float(floatstr_price) < float(price_limit):
                    writer.writerow([name, str_price, url])
            writer.writerow(['\n'])

            driver.close()
	
    time.sleep(1)
except Exception as e:
    print("HTTP status code  = {}({})".format(page.status_code,
                                              requests.status_codes._codes[page.status_code][0]))
    if (page.status_code != 200):
        os.remove(out_filename)
    else:
        print('ERROR FOUND while searching product ' +
              '"' + title + '"' + ' : ' + str(e))

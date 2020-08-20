# skroutz-web-scrap
[Skroutz](https://www.skroutz.gr/) Web Scraping using Selenium

Returns the skroutz shops in a .csv file that sell a product below client's desired price.  

**Execution**:  
```
$ python checkPrices-selenium.py Products.xlsx  
```

Input .xlsx file(e.g Products.xlsx) contains rows with:  
-Description (Name of the product)  
-Price (Maximum desired price)  
-skroutz URL for the current product 


**Requirements**:
:arrow_forward: Download Mozilla Firefox browser latest version
:arrow_forward: Download [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
:arrow_forward: Install *Python 3* 
:arrow_forward: Install the following libraries (or execute the program *install-python-libraries.py*):  
```
$ pip install xlrd  
$ pip install selenium  
$ pip install progressbar2 
```

:small_red_triangle: In order to use the program with Chrome browser, ChromeDriver is needed (and some modifications in code).  :small_red_triangle:


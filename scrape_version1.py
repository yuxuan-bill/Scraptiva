# Version 1.0 testing Demo
# Date： 2019/2/9

# This code is responsible for searching on Factiva
# This approach uses selenium package, it has nothing to do with Factiva's API
# Please be aware of the following before running:
#   1. Requires to log in and have the chrome memorized your log in information since we don't have an account
#   2. Change the initialization of chrome as needed
#   3. If the website design was changed by the publisher, this code will become useless

# Developer notes: requires update for NoSuchElement Exception

from time import sleep
from selenium.webdriver.common.action_chains import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver


# An example of the materials for demo
conm = 'AAR Corp'
role = 'CEO'
source = 'The New York Times'

url = 'http://guides.lib.uw.edu/factiva'

# initiate the driver
# Adjust as needed
# options.add_argument("--headless") can be added for better efficiency
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
driver = webdriver.Chrome(executable_path = path,chrome_options = options )

# open the website
# run into a bug if the website didn't respond in 10s (update later)
driver.get(url)
driver.implicitly_wait(10)

# Enter elements in search box
driver.find_element_by_name('ftx').send_keys(role)

# Enter the date range
driver.find_element_by_xpath("//select[@name='dr']/option[@value='Custom']").click()
driver.find_element_by_name('frm').send_keys(11)
driver.find_element_by_name('frd').send_keys(1)
driver.find_element_by_name('fry').send_keys(2014)
driver.find_element_by_name('tom').send_keys(12)
driver.find_element_by_name('tod').send_keys(31)
driver.find_element_by_name('toy').send_keys(2018)

# For StaleElementReferenceException in the Source and Company
def find(driver):
    element = driver.find_element_by_class_name('mnuItm')
    if element:
        return element
    else:
        return False

# Enter the Source
# The default is the first option that appears on the list
# Note: may run into a bug if it encounters NoSuchElementException (update later)
driver.find_element_by_xpath("//td[@id = 'scTab']/div[@class = 'pnlTabArrow']").click()
action = ActionChains(driver)
driver.find_element_by_id('scTxt').send_keys(source)
driver.find_element_by_id('scLkp').click()
element = WebDriverWait(driver,10).until(find)
element.click() # may have a bug, still testing
driver.find_element_by_class_name('mnuItm').click()
driver.find_element_by_xpath("//td[@id = 'scTab']/div[@class = 'pnlTabArrow']").click()

# Enter the Company
# The default is the first option that appears on the list
# Note: may run into a bug if it encounters NoSuchElementException (update later)
driver.find_element_by_xpath("//td[@id = 'coTab']/div[@class = 'pnlTabArrow']").click()
driver.find_element_by_id('coTxt').send_keys(conm)
driver.find_element_by_id('coLkp').click()
element = WebDriverWait(driver,10).until(find)
element.click() # may have a bug, still testing
driver.find_element_by_xpath("//td[@id = 'coTab']/div[@class = 'pnlTabArrow']").click()

# Search
# driver.find_element_by_name('ftx').send_keys(role, Keys.RETURN)
# print the current url
sleep(2)
driver.find_element_by_xpath("//li[@class = 'btn']/input[@value = 'Search']").click()
print('current url: %s' %driver.current_url)


# TODO: implement this method
# firm_name: string representing the name of company
# role: the role to search for, can take on two values: 'CEO' and 'CFO'
# pages: the resulting html files of articles that satisfy the search criteria, in the form of a list of strings
def get_article_pages(firm_name, role):
    pages = []

    return pages





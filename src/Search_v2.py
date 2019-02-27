# Version 1.1 testing Demo
# Date： 2019/2/21

# update notes:
#  1. updated error messages for unexpected bugs
#  2. updated sources requirement
#  2. updated output format

# This code is responsible for searching on Factiva
# This approach uses selenium package, it has nothing to do with Factiva's API
# Please be aware of the following before running:
#   1. Requires to log in and have the chrome memorized your log in information since we don't have an account
#   2. Change the initialization of chrome as needed
#   3. If the website design was changed by the publisher, this code will become useless

# Developer notes: Due to midterms, Still updating but in a SLOW progress

import sys
from time import sleep
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup
import src.config


# Input: information needed for search
# Output: A list of tuples with (link, html file). Empty list if no result.
def search(conm, role):
    print("Processing company " + conm + " with role " + role + "...")
    sources = src.config.search_criteria["sources"]
    url = 'http://guides.lib.uw.edu/factiva'
    if role == 'CEO':
        role = 'CEO or (Chief Executive)'
    else:  # conm = 'CFO'
        role = 'CFO or (Chief Financ)'

    # Error messages for unexpected bugs
    def error_message(message):
        print(message)
        print("Current progress: " + conm + ", " + role)

    # initiate the driver
    # Adjust as needed
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    if not src.config.headless:
        options.add_argument("--headless")
    path = src.config.chrome_webdriver_location
    try:
        driver = webdriver.Chrome(executable_path = path,chrome_options = options)
    except exceptions.WebDriverException:
        error_message("Error: Cannot locate your Google driver. Please edit the path.")
        sys.exit()

    # open the website
    # run into a bug if the website didn't respond in 10s (update later)
    driver.get(url)
    driver.implicitly_wait(20)

    # Enter elements in search box
    try:
        driver.find_element_by_class_name('ace_text-input').send_keys(role)
    except exceptions.NoSuchElementException:
        error_message("Timeout, unable to open the website due to internet error or login error.")
        sys.exit()

    # Enter the date range
    driver.find_element_by_xpath("//select[@name='dr']/option[@value='Custom']").click()
    for key, value in src.config.search_criteria['time'].items():
        driver.find_element_by_name(key).send_keys(value)

    # For StaleElementReferenceException in the Source and Company
    def find(driver):
        element = driver.find_element_by_class_name('mnuItm')
        if element:
            return element
        else:
            return False

    # Enter the Source
    # The default is the first option that appears on the list
    # Note: may run into a bug (update later)
    for source in sources:
        driver.find_element_by_xpath("//td[@id = 'scTab']/div[@class = 'pnlTabArrow']").click()
        sleep(1)
        driver.find_element_by_id('scTxt').send_keys(source)
        driver.find_element_by_id('scLkp').click()
        try:
            element = WebDriverWait(driver,20).until(find)
        except exceptions.TimeoutException:
            error_message("Error, cannot find the source named " + source)
            sys.exit()
        element.click() # may have a bug, still testing
        driver.find_element_by_class_name('mnuItm').click()
        driver.find_element_by_xpath("//td[@id = 'scTab']/div[@class = 'pnlTabArrow']").click()

    # Enter the Company
    # The default is the first option that appears on the list
    # Note: may run into a bug  (update later)
    driver.find_element_by_xpath("//td[@id = 'coTab']/div[@class = 'pnlTabArrow']").click()
    sleep(1)
    driver.find_element_by_id('coTxt').send_keys(conm)
    driver.find_element_by_id('coLkp').click()
    try:
        element = WebDriverWait(driver, 20).until(find)
    except exceptions.TimeoutException:
        error_message("Error, cannot find the company")
        sys.exit()
    element.click()  # may have a bug, still testing
    driver.find_element_by_xpath("//td[@id = 'coTab']/div[@class = 'pnlTabArrow']").click()

    # Search
    # driver.find_element_by_name('ftx').send_keys(role, Keys.RETURN)
    # print the current url
    sleep(1)
    driver.find_element_by_xpath("//li[@class = 'btn']/input[@value = 'Search']").click()
    driver.implicitly_wait(20)
    current_html = driver.page_source

    # html: the html page of search result
    # links: the links for articles in the form of a list
    # Return null if no articles found
    def get_article_links(html):
        links = []
        soup = BeautifulSoup(html, 'html.parser')
        entries = soup.findAll('tr', {'class': 'headline'})
        for entry in entries:
            links.append(entry.find_all('td')[2].find('a')['href'].replace('..', 'https://global.factiva.com'))
        return links

    links = get_article_links(current_html)
    result = []
    for link in links:
        driver.get(link)
        result.append((link, driver.page_source))
        sleep(5) # Don't delete
    driver.quit()
    return result

# An example of the materials for demo
# conm = 'AAR CORP'
# role = 'CEO or (Chief Executive)'
# results = search(conm,role)
# print(results)

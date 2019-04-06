import src.config as config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    # the following two options are added so that headless can work on mac
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.headless = True if config.headless else False
    driver = webdriver.Chrome(executable_path=config.chrome_webdriver_location, chrome_options=options)
    driver.implicitly_wait(config.implicit_wait_time)
    return driver


def enter_search_criteria(conm, role, driver):

    # Enter elements in search box
    driver.find_element_by_class_name('ace_text-input').send_keys(role)

    # Enter the date range
    driver.find_element_by_xpath("//select[@name='dr']/option[@value='Custom']").click()
    for key, value in config.search_criteria['time'].items():
        driver.find_element_by_name(key).send_keys(value)

    # Choose the Duplicate (Identical)
    driver.find_element_by_xpath("//select[@name='isrd']/option[@value='High']").click()

    # Enter the Source
    # The default is the first option that appears on the list, except for Fortune, which is the 5th
    driver.find_element_by_xpath("//td[@id = 'scTab']/div[@class = 'pnlTabArrow']").click()
    for source in config.search_criteria['sources']:
        sleep(0.1)
        element = driver.find_element_by_id('scTxt')
        element.send_keys(source)
        sleep(2)
        element.send_keys(Keys.ARROW_DOWN)
        if source == "Fortune":
            for i in range(4):
                element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)

    # Enter the Company
    # The default is the first option that appears on the list
    driver.find_element_by_xpath("//td[@id = 'coTab']/div[@class = 'pnlTabArrow']").click()
    sleep(0.1)
    element = driver.find_element_by_id('coTxt')
    element.send_keys(conm)
    sleep(2)
    element.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

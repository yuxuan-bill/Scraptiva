from src.SeleniumActions import *
from src.ContentFinder import *


# get all article pages related to specified company and role.
# return the resulting html files of articles that satisfy the search criteria, in the form of a list of strings
def get_article_pages(driver, conm, role):
    print("Processing company " + conm + " with role " + role + "...")

    driver.get("https://global.factiva.com/sb/default.aspx?lnep=hp")
    enter_search_criteria(conm, get_role_input(role), driver)

    # Search
    sleep(0.1)
    driver.find_element_by_xpath("//li[@class = 'btn']/input[@value = 'Search']").click()
    sleep(3)
    links = get_article_links(driver.page_source)
    result = []
    for i in range(0, len(links)):
        print("\tProcessing article " + str(i + 1) + " of total " + str(len(links)))
        driver.get(links[i])
        sleep(3)
        result.append(driver.page_source)
        # Factiva blocks you out if you search for articles too quickly
        sleep(5)
    return result


# return CEO or (Chief Executive) if role is CEO, CFO or (Chief Financ*) if role is CFO
def get_role_input(role):
    return 'CEO or (Chief Executive)' if role == 'CEO' else 'CFO or (Chief Financ*)'

# from src import Search_v2
#
#
# # firm_name: string representing the name of company
# # role: the role to search for, can take on two values: 'CEO' and 'CFO'
# # return: the resulting html files of articles that satisfy the search criteria, in the form of a list of strings
# def get_article_pages(firm_name, role):
#     try:
#         return Search_v2.search(firm_name, role)
#     except Exception:
#         print("Something went wrong")
#         return []

from src.SeleniumActions import *
from src.ContentFinder import *


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
    for link in links:
        print(link)
        driver.get(link)
        sleep(3)
        result.append(driver.page_source)
        # Factiva blocks you out if you search for articles too quickly
        sleep(5)
    return result


# return CEO or (Chief Executive) if role is CEO, CFO or (Chief Financ*) if role is CFO
def get_role_input(role):
    return 'CEO or (Chief Executive)' if role == 'CEO' else 'CFO or (Chief Financ*)'

# Generate a new csv file based on the information collected and the original firm list csv file.

import csv
from src.ContentFinder import get_content
from src.ArticleGetter import get_article_pages
from src.SeleniumActions import *
import src.config
import sys


# firm_list: the name of original firm_list csv file
# result_file_name: the name of file to store search result, if the file already exists, it will be truncated.
#
# This function processes each (company, role) at once, if an error occurs, it records the error in result csv file
# and go on with next company and role to process.
def generate_firm_list(firm_list_file, result_file_name):

    # login Factiva and only use one webdriver to increase speed
    driver = get_chrome_driver()
    driver.get('http://guides.lib.uw.edu/factiva')
    sleep(5)

    with open(firm_list_file, 'r') as firm_list:
        with open(result_file_name, "w+") as result:
            firm_list_reader = csv.DictReader(firm_list)
            result_writer = csv.DictWriter(result, fieldnames=firm_list_reader.fieldnames)
            result_writer.writeheader()
            for entry in firm_list_reader:
                try:
                    article_list = get_article_pages(driver, entry['conm'], entry['Role'][0:3])
                    entry_list = list()
                    for article in article_list:
                        article_info = get_content(article)
                        filled_entry = entry.copy()
                        for key in article_info:
                            filled_entry[key] = article_info[key]
                        entry_list.append(filled_entry)
                except Exception as e:
                    entry["Source"] = "-----ERROR WHEN PROCESSING-----"
                    result_writer.writerow(entry)
                    sys.stderr.write(str(e))
                else:
                    for filled_entry in entry_list:
                        result_writer.writerow(filled_entry)
                    if not entry_list:  # no articles for this role of company
                        result_writer.writerow(entry)
    driver.quit()


if __name__ == "__main__":
    generate_firm_list(src.config.firm_list_location, src.config.output_location)

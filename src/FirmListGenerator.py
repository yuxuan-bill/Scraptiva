# Generate a new csv file based on the information collected and the original firm list csv file.

import csv
from src.ContentFinder import get_content
from src.ArticleGetter import get_article_pages
import src.config as config
import json


# firm_list: the list of entries to search
# driver: selenium driver used in the scraping process
#
# This function processes each (company, role) at once, if an error occurs, it records the error in result csv file
# and go on with next company and role to process.
def generate_firm_list(firm_list, driver):
    with open(config.output_location, "a+", 1) as result:
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
            except Exception as err:
                with open(config.scrape_status_location, "w") as status_file:
                    status_dict = json.loads(status_file.read())
                    status_dict["error_list"].append(entry)
                    json.dump(status_dict, status_file)
                print(err)
                return 1
            else:
                for filled_entry in entry_list:
                    result_writer.writerow(filled_entry)
                if not entry_list:  # no articles for this role of company
                    result_writer.writerow(entry)
    return 0

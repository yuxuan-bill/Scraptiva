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
def generate_firm_list(process_list, driver):
    with open(config.output_location, "r") as header_reader:
        header = csv.DictReader(header_reader).fieldnames
    with open(config.output_location, "a+") as result:
        result_writer = csv.DictWriter(result, header)
        for entry in process_list:
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
                with open(config.scrape_status_location, "r") as status_file:
                    status_dict = json.loads(status_file.read())
                status_dict["error_list"].append(entry)
                with open(config.scrape_status_location, "w") as status_writer:
                    json.dump(status_dict, status_writer)
                print(err)
            else:
                result_writer.writerows(entry_list)
                if not entry_list:  # no articles for this role of company
                    result_writer.writerow(entry)

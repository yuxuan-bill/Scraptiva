# Generate a new csv file based on the information collected and the original firm list csv file.

import csv
from src.ContentFinder import get_content
from src.ArticleGetter import get_article_pages
import src.config


# firm_list: the name of original firm_list csv file
# result_file_name: the name of file to store search result, if the file already exists, it will be truncated.
def generate_firm_list(firm_list_file, result_file_name):
    with open(firm_list_file, 'r') as firm_list:
        with open(result_file_name, "w+") as result:
            firm_list_reader = csv.DictReader(firm_list)
            result_writer = csv.DictWriter(result, fieldnames=firm_list_reader.fieldnames)
            result_writer.writeheader()
            for entry in firm_list_reader:
                article_list = get_article_pages(entry['conm'], entry['Role'][0:3])
                if not article_list:
                    result_writer.writerow(entry)
                for article in article_list:
                    article_info = get_content(article)
                    for key in article_info:
                        entry[key] = article_info[key]
                    result_writer.writerow(entry)


if __name__ == "__main__":
    generate_firm_list(src.config.firm_list_location, src.config.output_location)

import csv
import json
from src.SeleniumActions import *
from src.FirmListGenerator import generate_firm_list


# Process several entries in the given firm list, the exact number of entries to process is specified in config.
# firm_list_file: firm list file location, output_file: the result file this process will write to
def get_process_list():
    process_list = list()
    with open(config.firm_list_location, 'r') as firm_list:
        with open(config.scrape_status_location, 'w+') as status_file:
            reader = csv.DictReader(firm_list)
            count = 0
            record = False
            status_dict = json.loads(status_file.read())
            next_entry = status_dict["next"]
            for entry in reader:
                if entry["gvkey"] == next_entry[0] and entry['Role'] == next_entry[1][0:3]:
                    record = True
                if record and count <= config.entries_to_process:
                    process_list.append(entry)
                else:
                    status_dict["next"] = entry
                    json.dump(status_dict, status_file)
                    break
    # potential risk: if "next" in scrape_status is updated but for some reason the returned process_list
    # is not processed nor recorded in the error_list, these entries are lost.
    return process_list


# Start the scraping process. The workflow is as the following:
# for 0 : process_times:
#     try re-scrape entries that led to errors in last scrape for 5 times
#     if they all fail:
#         exit
#     process entries_to_process entries
def process():

    # login Factiva and only use one webdriver to increase speed
    # may result in a bug if login fails
    driver = get_chrome_driver()
    driver.get('http://guides.lib.uw.edu/factiva')
    sleep(5)

    for _ in range(config.process_times):
        with open(config.scrape_status_location, 'w') as status:

            # retrieve the error list and re-initiate the error list to be empty
            status_dict = json.loads(status.read())
            error_list = status_dict["error_list"]
            status_dict["error_list"] = []
            json.dump(status_dict, status)
            status.flush()

            attempt_count = 0
            while error_list:
                print("Processing " + str(len(error_list)) + " unfinished entries from last scrape...")
                generate_firm_list(error_list, driver)
                attempt_count += 1
                if attempt_count >= 5:
                    driver.quit()
                    print("The error entries in last scrape cannot be scraped")
                    return
            print("Processing " + str(config.entries_to_process) + " entries...")
            generate_firm_list(get_process_list(), driver)
    driver.quit()

# TODO: 1. add init for scrape_status 2. add quit function

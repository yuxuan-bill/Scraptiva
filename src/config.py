search_criteria = {
    'time': {  # from mm/dd/yyyy to mm/dd/yyyy
        'frm': 1,
        'frd': 1,
        'fry': 2013,
        'tom': 12,
        'tod': 31,
        'toy': 2017
    },
    'sources': ['The New York Times', 'Financial Times', 'The economist', 'Forbes', 'Fortune', 'The Times',
                'The Wall Street Journal'],
}

implicit_wait_time = 10

chrome_webdriver_location = '/Users/luyuxuan/Desktop/scrape/chromedriver'

firm_list_location = "/Users/luyuxuan/Desktop/scrape/Scraptiva/short_firmlist.csv"

output_location = "/Users/luyuxuan/Desktop/scrape/Scraptiva/test_result.csv"

scrape_status_location = "/Users/luyuxuan/Desktop/scrape/Scraptiva/src/scrape_status.json"

entries_to_process = 2

process_times = 1

headless = False


if __name__ == "__main__":
    from src.Processor import process
    process()

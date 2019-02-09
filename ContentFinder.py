
# From a Factiva search result page, get the following information for each of the articles:
# 1. the source of article,
# 2. its date, time,
# 3. title,
# 4. and content.

from bs4 import BeautifulSoup
import json

HTML_DOC = open("test.html", 'r', encoding = 'utf-8')

soup = BeautifulSoup(HTML_DOC, 'html.parser')
entries = soup.findAll('tr', {'class': 'headline'})

# list of dictionary, e.g. [{url: --, date: --, time: --, title: --, content: --}, {...}, ...]
articleInfo = []
for entry in entries:
    simplifiedEntry = entry.find_all('td')
    # contains headline, date'n'time
    entry1 = simplifiedEntry[0].find('input')['data-metrics-data']
    # contains url to content
    entry2 = simplifiedEntry[2].find('a')

    print(entry1)
    print(entry2)
    print()


    #simplifiedEntry = list(BeautifulSoup(entry, 'html.parser').findAll('td')[i] for i in [0, 2])
    #print(simplifiedEntry)
    #print()


# From a Factiva search result page, get the following information for each of the articles:
# 1. the source of article,
# 2. its date, time,
# 3. title,
# 4. url,
# 5. and content.

from bs4 import BeautifulSoup
import json
import urllib.request
import ssl

# resolve certificate verify failed error,
# see: https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
context = ssl._create_unverified_context()

HTML_DOC = open("test.html", 'r', encoding='utf-8')

soup = BeautifulSoup(HTML_DOC, 'html.parser')
entries = soup.findAll('tr', {'class': 'headline'})

# list of dictionary, e.g. [{url: --, source: --, date: --, time: --, title: --, content: --}, {...}, ...]
articleInfo = []
for entry in entries:
    simplifiedEntry = entry.find_all('td')
    # contains headline, date'n'time
    entry1 = json.loads(simplifiedEntry[0].find('input')['data-metrics-data'])
    # contains url to content
    entry2 = simplifiedEntry[2]

    title = entry1['Hdl']
    (time, date) = entry1['Pd'].split(", ")
    url = entry2.find('a')['href'].replace('..', 'https://global.factiva.com')
    source = entry2.find(class_='leadFields').find('a').text
    # html file that contains the article content
    # TODO: may fail parsing in case this article is only available on some third party website
    print(url)
    contentHtml = urllib.request.urlopen(url, context=context).read().decode('utf8')
    contentSoup = BeautifulSoup(contentHtml, 'html.parser') # TODO: get intermediate page instead of final result
    print(contentSoup)
    print("--------------------")


    #simplifiedEntry = list(BeautifulSoup(entry, 'html.parser').findAll('td')[i] for i in [0, 2])
    #print(simplifiedEntry)
    #print()

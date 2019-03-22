# From a Factiva article page, get the following information about the article:
# 1. its date,
# 2. time,
# 3. title,
# 4. and content.

from bs4 import BeautifulSoup
from bs4 import element


# html: a string that stores the page source code
# return: a dictionary of content information about the article, in the form
#       {Date: --, Time: --, Title: --, Source: --, Content: --}, paragraphs are separated using ' | '
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    article_container = soup.find("div", {"class": "article enArticle"})
    header = article_container.findAll("div", {"class": None})
    print(header)
    # sometimes Factiva article pages vary in format, this solves the problem that article
    # title is not the first div found
    if not header[0].get("id"):
        header.pop(0)
    article_info = dict()
    article_info["Title"] = header[0].find("span").string
    article_info["Date"] = header[2].string
    # this solves the problem that sometimes the time of the article is not available
    if len(str(header[3].string)) > 5:
        header.insert(3, "Not available")
    article_info["Time"] = header[3].string if isinstance(header[3], element.Tag) else header[3]
    article_info["Source"] = header[4].string
    content = list(paragraph.getText()
                   for paragraph in
                   article_container.findAll("p", {"class": "articleParagraph enarticleParagraph"}))
    article_info["Content"] = " | ".join(content)
    return article_info


# html: the html page of search result
# links: the links for articles in the form of a list
# Return null if no articles found
def get_article_links(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    entries = soup.findAll('tr', {'class': 'headline'})
    for entry in entries:
        links.append(entry.find_all('td')[2].find('a')['href'].replace('..', 'https://global.factiva.com'))
    return links

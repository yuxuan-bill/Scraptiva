# From a Factiva article page, get the following information about the article:
# 1. its date,
# 2. time,
# 3. title,
# 4. and content.

from bs4 import BeautifulSoup


# html: a string that stores the page source code
# return: a dictionary of content information about the article, in the form
#       {source: --, date: --, time: --, title: --, content: [--, --, ...]}
def getContent(html):
    soup = BeautifulSoup(html, 'html.parser')
    article_container = soup.find("div", {"class": "article enArticle"})
    header = article_container.findAll("div", {"class": None})
    article_info = {}
    article_info["title"] = header[1].find("span").string
    article_info["date"] = header[3].string
    article_info["time"] = header[4].string
    article_info["content"] = list(paragraph.getText() for paragraph in article_container.findAll("p", {"class": "articleParagraph enarticleParagraph"}))
    return article_info

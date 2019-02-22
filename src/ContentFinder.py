# From a Factiva article page, get the following information about the article:
# 1. its date,
# 2. time,
# 3. title,
# 4. and content.

from bs4 import BeautifulSoup


# html: a string that stores the page source code
# return: a dictionary of content information about the article, in the form
#       {Date: --, Time: --, Title: --, Content: --}, paragraphs are separated using ' | '
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    article_container = soup.find("div", {"class": "article enArticle"})
    header = article_container.findAll("div", {"class": None})
    article_info = dict()
    article_info["Title"] = header[1].find("span").string
    article_info["Date"] = header[3].string
    article_info["Time"] = header[4].string
    content = list(paragraph.getText()
                   for paragraph in
                   article_container.findAll("p", {"class": "articleParagraph enarticleParagraph"}))
    article_info["Content"] = " | ".join(content)
    return article_info


if __name__ == "__main__":
    print(get_content(open("/Users/luyuxuan/Desktop/scrape/Scraptiva/factiva_article.html", 'r'))['Content'])

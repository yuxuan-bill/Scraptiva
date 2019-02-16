# from selenium import webdriver
# browser = webdriver.Chrome('/Users/luyuxuan/Desktop/scrape/chromedriver')
# html = browser.get('http://guides.lib.uw.edu/factiva')
# print(html.page_source)
# browser.get('https://global.factiva.com/du/article.aspx/?accessionno=RSTPROPE20181025eeap001b9&fcpil=en&napc=S&sa_from=&cat=a')


from selenium import webdriver


driver = webdriver.Chrome('/Users/luyuxuan/Desktop/scrape/chromedriver')
driver.implicitly_wait(10)
driver.get('https://global.factiva.com/du/article.aspx/?accessionno=RSTPROPE20181025eeap001b9&fcpil=en&napc=S&sa_from=&cat=a')

html = driver.page_source
print(html)

import urllib.request
from bs4 import BeautifulSoup
import ssl




if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    theurl = "https://blogs.wsj.com/cfo/2016/07/14/cfo-moves-aar-corp-fairpoint-communications/"
    thepage = urllib.request.urlopen(theurl)
    soup = BeautifulSoup(thepage, "html.parser")
    print(soup.title.text)

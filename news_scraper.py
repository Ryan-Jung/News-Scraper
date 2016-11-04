import requests
import html5lib
from bs4 import BeautifulSoup

class ScrapeNews:
    _URL = "http://www.sfgate.com"

    def __init__(self):
        self.data = self.scrape()

    def scrape(self):
        """Scrapes the latest news in htpp://www.sfgate.com
        """
        html = requests.get(self._URL).content
        
        soup = BeautifulSoup(html, "html5lib")
        #Stores the urls to the articles
        url_list = []
        #An article's url should be stored in the same index of the url_list
        article_list = []

        latestNewsContainer = soup.find("div","core-headline-list aboutsfgate")

        for link in latestNewsContainer.find_all("a", class_="hdn-analytics"):
            if link.has_attr("href"):
                    url = link["href"].encode("ascii", "ignore")
                    url_list.append(self._full_URL(url))
                    article_list.append(link.string.encode("ascii", 'ignore'))
        return {'articles' : article_list, 'urls' : url_list}        
    


    def _full_URL(self, url):
        """Adds the base url if the link is not a full url.
        """
        fullURL = url
        if url[0] == "/":
            fullURL = self._URL + url
            return fullURL



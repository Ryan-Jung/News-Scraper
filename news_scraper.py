import requests
import html5lib
from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod

"""
Contains all the data gathered by the various ArticleScrapers
"""
class ScrapeNews():
	def __init__(self):
		self.data = self.scrapeAll()
		
	def scrapeAll(self):
		"""Adds each ArticleScraper's article list and url list together and returns
		a dictionary {"articles": article_list, "urls", url_list}
		"""
		websiteScrapers = [SFGateScraper(),]
		
		articles = []
		urls = []
		
		for index in range(len(websiteScrapers)):
			scraper = websiteScrapers[index]

			articles.extend(scraper.data["articles"])
			urls.extend(scraper.data["urls"])
		
		return {"articles": articles, "urls": urls}
"""
An abstract class that all article scrapers should inherit
"""
class ArticleScraper:
	__metaclass__ = ABCMeta

	def __init__(self):
		self.data = self.scrape()
	
	@abstractmethod
	def scrape(self):
		"""Should return articles in a dict -> {articles: article_list, urls: url_list}. 
			The url_list should contain a full url rather than a relative url.
		"""
		raise NotImplementedError()
	
	

"""
An article scraper for www.sfgate.com
"""
class SFGateScraper(ArticleScraper):
	_URL = "http://www.sfgate.com"

	
	def __init__(self):
		super(SFGateScraper,self).__init__()
		
		
	def scrape(self):
		"""Scrapes the latest news section in htpp://www.sfgate.com"""
		html = requests.get(self._URL).content

		soup = BeautifulSoup(html, "html5lib")
		
		url_list = []
		article_list = []

		latestNewsContainer = soup.find("div","core-headline-list aboutsfgate")

		for link in latestNewsContainer.find_all("a", class_="hdn-analytics"):
			if link.has_attr("href"):
				url = link["href"].encode("ascii", "ignore")
				url_list.append(self._full_URL(url))
				article_list.append(link.string.encode("ascii", 'ignore'))
		return {'articles' : article_list, 'urls' : url_list}        
    


	def _full_URL(self, url):
		"""Adds the base url if the link is not a full url."""
		fullURL = url
		
		if url[0] == "/":
			fullURL = self._URL + url
			return fullURL
			


			




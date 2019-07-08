# WebScrapingProject

## OBJECTIVE


The objective of this project is to perform webscraping of scientific articles in the area of machine learning from two main sources: 
- Journal of Machine Learning Research (https://jmlr.org/) : 2000 - 2018
- NIPS conference (https://papers.nips.cc/) : 1987 - 2018

and analyze this data in Python using natural language processing (NLP). 

## WHAT HAS BEEN DONE

1) Using scrapy Spider, I created two classes: jmlr_spider to scrape JMLR journal website and nips_spider to NIPS conference website. In total, with scrapy 
spiders I downloaded over 10,000 articles. Dataset articles.csv contains the following information: Abstract, Authors, Journal_Conference, Pdf_url, Title, Volume, Year
2) Using Selenium package, I perform scraping of google scholar (https://scholar.google.com/) to get article citation data and information about authors. Article citations are stored in the file title_citations.csv. Information about authors is scraped into file authors.csv, which contains the following fields: google_scholar_id, name, citations, h_index. In attempt to scrape google scholar website without being blocked, I am using proxies stored in the file proxies.txt
3) Perform basic analytics and natural language processing (NLP) on articles data

## FILES IN A PROJECT


### scrapy Spider:

jmlr_spider.py, nips_spider.py contain spiders for JMLR and NIPS websites; auxiliary files - items.py, middlewares.py, pipelines.py, settings.py, __init__.py

### Selenium:

selenium_wrapper.py contains SeleniumWrapper class that handles scraping google scholar,
proxy.txt - contains over 2,500 of proxy ip-addresses used by Selenium

### Class Articles:

articles_library.py contains class Articles that conceptualize data in object-oriented framework and contains methods to handle data

### Main notebook:

main.ipynb - jupyter notebook sources classes in selenium_wrapper.py and articles_library.py; all objects are initialized here and methods are called

### Data Files:
articles.csv - contains article data from JMLR and NIPS websites with the following fields: Abstract, Authors, Journal_Conference, Pdf_url, Title, Volume, Year

title_citations.csv - contains citations of articles from google scholar with Title, Citations fields

authors.csv - contains authors information from google scholar with google_scholar_id, name, citations, h_index fields

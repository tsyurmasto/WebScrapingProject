from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
import time
import pandas as pd
import random 

class SeleniumWrapper(object):
	def __init__(self,filename_proxies,filepath_chrome):
		with open(filename_proxies,'r') as file:
			self.__proxies_lst = file.read().split(',')
		self.__filepath_chrome = filepath_chrome
   	# configure driver function
	def configure_driver(self,ip_address):
		options = webdriver.ChromeOptions() # add options to chrome such as hide mode, change user settings, etc.
		options.add_argument('headless') # hide chrome mode while scraping
		proxy = Proxy()
		proxy.proxyType = ProxyType.MANUAL
		proxy.autodetect = False
		proxy.httpProxy = proxy.sslProxy = proxy.socksProxy = ip_address
		options.Proxy = proxy
		options.add_argument("ignore-certificate-errors")
		driver = webdriver.Chrome(self.__filepath_chrome,chrome_options=options)
		return(driver)
   
   	# parse google scholar page
	def parse_google_scholar_page(self,driver, title):    
		# initialize page
		driver.get('https://scholar.google.com/')
		# get elements
		input_element = driver.find_element_by_xpath('//*[@class="gs_in_txt gs_in_ac"]')
		submit_element = driver.find_element_by_xpath('//*[@id="gs_hdr_tsb"]')
		# check if text_box has a string, in which case clear it
		if len(input_element.get_attribute('value')) > 0:
			input_element.clear()
		# type author into textbox
		input_element.send_keys(title)
		# click sumbit
		submit_element.click()
		# get number of citations
		citation_element = driver.find_elements_by_xpath('//div[@class="gs_fl"]/a')
		if (len(citation_element) > 0):
			# extract number of citation in text format
			citation_text = citation_element[2].text.replace('Cited by ','')
			# check if citation number exists        
			citation_text
		else: np.nan
		# get authors dictionary
		authors_element = driver.find_elements_by_xpath('//div[@class="gs_r gs_or gs_scl"][1]//div[@class="gs_a"]/a')
		authors_url = []    
		for item in authors_element:
			name = item.text
			authors_url += [item.get_attribute('href')]
		return((citation_text,authors_url)) 
   
   	# parse author's page
	def parse_author_page(self,driver, url):
		driver.get(url)
		name = driver.find_element_by_xpath('//div[@id="gsc_prf_in"]').text
		elements = driver.find_elements_by_xpath('//td[@class="gsc_rsb_std"]')
		citations = elements[0].text
		h_index = elements[2].text
		google_scholar_id = url.replace('https://scholar.google.com/citations?user=','')
		return({'google_scholar_id':google_scholar_id,'name':name,'citations':citations,'h_index':h_index}) 
   
   	# main parser of the class
	def selenium_parse(self,title_lst):
		# create pandas Sereies for title citations
		title_citations_series = pd.Series(index=title_lst)
		# create pandas dataframe for authors with columns: google_scholar_id, name, citations, h_index
		authors_citations_df = pd.DataFrame(columns=['google_scholar_id','name','citations','h_index'])
		# initialize counter
		title_counter = 1
		run_counter = 1    
		for title in title_lst:
			# configure a driver by randomly selecting an ip_address from a list of proxies
			ip_address = random.sample(self.__proxies_lst,1)
			driver = self.configure_driver(ip_address)
			# parse google scholar page
			try:
				(title_citations,urls) = self.parse_google_scholar_page(driver, title)
				title_citations_series[title] = title_citations            				
				print('title_counter={}'.format(title_counter)+','+ 'run_counter={}'.format(run_counter)+','+
					'proxy={}'.format(ip_address)+','+ 'response={}'.format(requests.get('https://scholar.google.com/').status_code))												
			except Exception as e:
				print(e)   
			driver.close()
			# parse author's page
			for url in urls:
				# configure a driver by randomly selecting an ip_address from a list of proxies
				ip_address = random.sample(self.__proxies_lst,1)
				driver = self.configure_driver(ip_address)            
				# for each url parse the author's page
				try:
					author_dict = self.parse_author_page(driver, url)
					authors_citations_df = authors_citations_df.append(pd.Series(author_dict),ignore_index=True)					
					print('title_counter={}'.format(title_counter)+','+ 'run_counter={}'.format(run_counter)+','+
						'proxy={}'.format(ip_address)+','+ 'response={}'.format(requests.get(url).status_code))
					run_counter += 1
				except Exception as e:
					print(e)   
				driver.close()									
				run_counter += 1
			# print with a step of 10 titles
			if (title_counter % 10 == 0 or title_counter == len(title_lst)): 
				title_citations_series.to_csv('title_citations.csv')
				authors_citations_df.to_csv('authors.csv',index=False)
			# increament counter
			title_counter += 1
		return(title_citations_series,authors_citations_df)
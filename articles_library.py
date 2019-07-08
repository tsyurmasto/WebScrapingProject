import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer

class Articles(object):
	# initialize object of class
	def __init__(self,filename='articles.csv'):
		self.__df = pd.read_csv(filename)
	# function returns sample of n rows in dataframe
	def sample(self,n):
		return(self.__df.sample(n))
	# column to list
	def col_to_list(self,col): return(self.__df[col].tolist())		
	# fills 'Abstract Missing' in column 'Abstract' by empty string 
	def fill_missing_data(self):
		self.__df['Abstract'] = self.__df['Abstract'].apply(lambda x: '' if x=='Abstract Missing' else x)
	# convert title and abstract to lower cases	
	def to_lower(self):
		self.__df['Abstract'] = self.__df['Abstract'].str.lower()
		self.__df['Title'] = self.__df['Title'].str.lower()
	def filter(self):
		# remove punctuation from abstract
		self.__df['Abstract'] = self.__df['Abstract'].apply(lambda x: re.sub('[^\w\s]', '', x))
		# remove stopwords from abstract
		stop = stopwords.words('english')
		self.__df['Abstract'] = self.__df['Abstract'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))		
	# lemmatize sentence consisting of words seperated by spaces
	def lemmatize_sentence(self,sentence): 
		lemtzr = WordNetLemmatizer()
		lst = list(map(lambda x: lemtzr.lemmatize(x),sentence.split()))		
		return(' '.join(lst))
	# perform lemmatization on titles and abstracts	of type pandas.Series
	def lemmatize(self):			
		#self.__df['Abstract'] = self.__df['Abstract'].apply(lambda x: lemmatize_sentence(x))
		self.__df['Title'] = self.__df['Title'].apply(lambda x: self.lemmatize_sentence(x))
	def preprocess(self):
		# fill missing data
		self.fill_missing_data()
		# convert abstract and title to lower case
		self.to_lower()
		# filter
		self.filter()
	# number of rows in dataframe
	def nrows(self): return(self.__df.shape[0])
	# extracts all authors appeared in articles into a 	list
	def get_set_authors(self):
		# convert series data into list
		lst = self.__df['Authors'].tolist()
		# flatten nested list
		lst = list(map(lambda x: x.split(',')[0], lst))
		# remove duplicates
		lst = list(set(lst))
		# return list
		return(lst) 
	# function returns tuple of all authors sorted by frequency of articles
	def authors_freq(self):
		# convert series data into list
		lst = self.__df['Authors'].tolist()
		# flatten nested list
		lst_flatten = list(map(lambda x: x.split(',')[0], lst))
		# get distinct list authors
		lst_set = set(lst_flatten)	
		# create dictionary of authors
		authors_freq = {item:0 for item in lst_set}
		# calculate frequencies of authors
		for item in lst_flatten: authors_freq[item] += 1
		# most freq authors
		authors_freq_sorted = sorted(authors_freq.items(), key = lambda x: x[1], reverse = True)
		return(authors_freq_sorted)

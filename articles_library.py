import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer

class Articles(object):
	# initialize object of class
	def __init__(self,filename='articles.csv'):
		self.__df = pd.read_csv(filename)
	# number of rows in dataframe
	def nrows(self): return(self.__df.shape[0])
	# function returns a random sample of n rows in dataframe
	def sample(self,n):
		return(self.__df.sample(n))
	# column to series
	def col_to_series(self,col): return(self.__df[col])
	# column to list
	def col_to_list(self,col): return(self.__df[col].tolist())			
	# fills 'Abstract Missing' in column 'Abstract' by empty string 
	def fill_missing_data(self):
		self.__df['Abstract'] = self.__df['Abstract'].apply(lambda x: '' if x=='Abstract Missing' else x)
	# convert column to lower case
	def to_lower(self,col):
		self.__df.loc[:,col] = self.__df.loc[:,col].str.lower()
	# remove punctuation from column
	def remove_punctuation(self,col):	
		self.__df.loc[:,col] = self.__df.loc[:,col].apply(lambda x: re.sub('[^\w\s]', '', x))
	# remove stopwords from col
	def remove_stopwords(self,col):
		stop = stopwords.words('english')
		self.__df[col] = self.__df[col].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
	# lemmatize sentence consisting of words seperated by spaces
	def lemmatize_sentence(self,sentence): 
		lemtzr = WordNetLemmatizer()
		lst = list(map(lambda x: lemtzr.lemmatize(x),sentence.split()))		
		return(' '.join(lst))
	# perform lemmatization
	def lemmatize(self,col):					
		self.__df[col] = self.__df[col].apply(lambda x: self.lemmatize_sentence(x))
	# N-gram function
	def ngrams(self,lst,n): return(list( map(lambda x: ' '.join(list(x)), zip(*[lst[i:] for i in range(n)])) ))	
	# search articles by keywords
	# input: keywords in string format
	# output: dataframe with subset of articles
	def search_by_keywords(self,keywords,inTitle=True,inAbstract=False):
		mask_inTitle = list(map(lambda x: keywords in x,self.__df['Title'].tolist()))
		if inAbstract == False:
			mask = mask_inTitle
		else:
			mask_inAbstract = list(map(lambda x: keywords in x,self.__df['Title'].tolist()))
			mask = [x or y for a, b in zip(mask_inTitle,mask_inAbstract)]
		return(self.__df[mask])
	# extracts all authors that appeared in articles into a list
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
	# function returns a sorted tuple of ngrams together with frequencies, where ngrams are specified by ngrams_lst
	def title_freq(self,year=None,ngrams_lst=[1,2,3]):
		# filter by year
		# lst - list of all titles
		if (year == None):
			lst = self.col_to_list('Title')
		else:
			df = self.__df.loc[:,['Title','Year']]
			df.loc[:,'Year'] = df['Year'].apply(int)
			lst = df[df['Year'] == int(year)]['Title'].tolist()					
		lst_all = []
		# lst_all - list of ngrams titles
		for n in ngrams_lst:
			lst_all += list(map(lambda x: self.ngrams(x.split(),n), lst))
		# flatten list
		lst_all = [item for sublist in lst_all for item in sublist]
		lst_all_set = set(lst_all)
		# create a dictionary of words
		word_freq = {item:0 for item in lst_all_set}
		# calculate frequencies of authors
		for item in lst_all: word_freq[item] += 1
		# most freq words
		words_freq_sorted = sorted(word_freq.items(), key = lambda x: x[1], reverse = True)
		return(words_freq_sorted)
	# function returns a sorted tuple of ngrams together with frequencies, where ngrams are specified by ngrams_lst
	def abstract_freq(self,year=None,ngrams_lst=[1,2,3]):
		# filter by year
		# lst - list of all titles
		if (year == None):
			lst = self.col_to_series('Abstract').dropna().tolist()
		else:
			df = self.__df.loc[:,['Abstract','Year']]
			df.dropna(inplace=True)
			df.loc[:,'Year'] = df['Year'].apply(int)
			lst = df[df['Year'] == int(year)]['Abstract'].tolist()					
		lst_all = []
		# lst_all - list of ngrams titles
		for n in ngrams_lst:
			lst_all += list(map(lambda x: self.ngrams(x.split(),n), lst))
		# flatten list
		lst_all = [item for sublist in lst_all for item in sublist]
		lst_all_set = set(lst_all)
		# create a dictionary of words
		word_freq = {item:0 for item in lst_all_set}
		# calculate frequencies of authors
		for item in lst_all: word_freq[item] += 1
		# most freq words
		words_freq_sorted = sorted(word_freq.items(), key = lambda x: x[1], reverse = True)
		return(words_freq_sorted)
	# generate word cloud
	def title_word_cloud(self,year=None,ngrams_lst=[1,2,3]):
		# filter by year
		# lst - list of all titles
		if (year == None):
			lst = self.col_to_list('Title')
		else:
			df = self.__df.loc[:,['Title','Year']]
			df.loc[:,'Year'] = df['Year'].apply(int)
			lst = df[df['Year'] == int(year)]['Title'].tolist()					
		lst_all = []
		# lst_all - list of ngrams titles
		for n in ngrams_lst:
			lst_all += list(map(lambda x: self.ngrams(x.split(),n), lst))
		# flatten list
		lst_all = [item for sublist in lst_all for item in sublist]
		return(lst_all)

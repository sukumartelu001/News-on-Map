#!/usr/bin/python
import sys
import json
from bs4 import BeautifulSoup
import urllib2
import requests
import simplejson



#function to extract location and short text from the short article.
def get_location(link):
	url_short=link
	page_short=urllib2.urlopen(url_short)
	soup_short = BeautifulSoup(page_short.read())
	paragraph_text=soup_short.findAll('p')
	result = []
	
	for each_paragraph in paragraph_text:
		if "(Reuters)" in each_paragraph.string:
			
			#extract the location
			list = each_paragraph.string.split('(')
			result.append(list[0])
			result.append(each_paragraph.string)

			return result

	result.append("None")
	result.append("None")
	return result

#end of function

#function to get coordinates from mapquest.
def get_coords(location):
	mapquest_url = 'http://open.mapquestapi.com/nominatim/v1/search.php?format=json&limit=1&q='+location

	mapq = requests.get(mapquest_url)
	content = mapq.content
	geo = simplejson.loads(content)
	coord = []
	
	#if object returned is empty, set lat and lon to None
	if not geo:
		coord.append('None')
		coord.append('None')
		return coord
	
	for item in geo:
		coord.append(item['lat'])
		coord.append(item['lon'])
		return coord
#end of function


news_list = []
news = {}


for i in range(1,3,1): 
	#url = 'http://us.mobile.reuters.com/category/worldNews?p='+str(i)
	url = 'http://us.mobile.reuters.com/category/internetNews?p='+str(i)
	#url = 'http://us.mobile.reuters.com/category/technologyNews?p='+str(i)
	#url = 'http://us.mobile.reuters.com/category/scienceNews?p='+str(i)
	#load page
	page = urllib2.urlopen(url)
	#read page to soup variable
	soup = BeautifulSoup(page.read())
	
	#extract all links from the category pages, then call get_location to get the location
	for item in soup.findAll("span", { "class" : "lnkart" }):
		news_item = item.find('a')
		
		link = "http://us.mobile.reuters.com"+news_item.get('href')
		headline = news_item.get_text()

		if (' '.join(headline.split()) == "Next 10 Headlines") or (' '.join(headline.split()) == "Previous 10 Headlines"):
			print "gotcha"
		else:
			#calling get_location to get location from short article
			print '------------------------------------------------------------------------------'
			print link
			results = get_location(link)
			location = results[0]
			short_text = results[1]

			#calling get_coords to get coordinates
			if ( location != "") or ( location != "None"):
				coords = get_coords(location)
				lat = coords[0]
				lon = coords[1]
					
				news = { 'headline':headline, 'weblink': link, 'short_text': short_text, 'location': location, 'lat': lat, 'lon': lon }
				news_list.append(news)
	
			print news

print 'INDENT:', json.dumps(news_list, sort_keys=True, indent=2)

#write contents of 'news' to data.json file
with open('internet.json', mode='w') as f:
  json.dump(news_list, f)


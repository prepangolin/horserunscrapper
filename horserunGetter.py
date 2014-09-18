#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Jing Wang.
from BeautifulSoup import BeautifulSoup as BS
import re, time
from selenium import webdriver
#------------------------------------------------------------

Url = 'http://www.bbc.com/sport/horse-racing/uk-ireland/results'
euro2gpbUrl = 'http://www.eurotogbp.co.uk/'

def download_page(url, data=None):
	driver = webdriver.Firefox()
	conn = driver.get(url)
	resp = BS(driver.page_source)

	return resp

def getRate(url, data=None):
    # Must check cache using httplib2 here!    
    soap = download_page(url)
    extractTxt = soap.find('p', attrs={"style":"margin-bottom: 0px; color: #666666;"}).text
    extractRate = re.compile('= (.*?) ')

    return float(extractRate.search(extractTxt).group(0)[2:])

def read_file(file):
	fp = open(file)
	return fp.read()

def change_rate(euro, rate):
	gpb = euro * rate	
	return gpb

exchangeRate = getRate(euro2gpbUrl)
time.sleep(5)
soap = download_page(Url)
#soap = BS(read_file("test.html"))
fp = open("result.txt", "w")
for item in soap.findAll("table"):	
	meetingItem = item.parent.find('h2', attrs={"class":"table-header"})
	meetingName = meetingItem.text
	meetingChild = meetingItem.findChild().text
	meetingName = meetingName.split(meetingChild)[0]
	
	for body in item.findAll('tbody'):		
		for entry in body.findAll('tr'):
			meetingTime = entry.find('td', attrs={"class":"race-time"}).text
			results = entry.find('td', attrs={"class":"result"})
			places = results.findAll('span', attrs={"class":"pos"})
			fp.write("\n")
			fp.write( "%s\n" %(meetingName))
			fp.write( "%s\n" %(meetingTime))
			for element in places:
				number = element.text[:1]
				jockey = element.findNextSibling().findNextSibling().text[1:-1]				
				fp.write( "%s %s\n" %(number, jockey))
			
			route = results.find('span', attrs={"class":"distances"})
			if route is not None:
				route = route.text[10:].encode('utf-8')
				fp.write( "%s\n" %(route))
			
			ret = entry.find('td', attrs={"class":"return"})
			betItems = ret.findAll('span', attrs={"class":"bet-name"})
			for betItem in betItems:
				if cmp(betItem.text, 'Exacta:') == 0:
					betValue = betItem.findNextSibling().text.encode('utf-8')					
					if cmp('\xc2\xa3', betValue[:2]) == 0:
						betValue = betValue[2:]
						fp.write( "Exacta %s\n" %(betValue))
					if cmp('\xe2\x82', betValue[:2]) == 0:						
						betValue = betValue[3:]
						betValue = str(change_rate(float(betValue), exchangeRate))					
						fp.write( "Exacta %s\n" %(betValue))
				elif cmp(betItem.text, 'CSF:') == 0:
					betValue = betItem.findNextSibling().text.encode('utf-8')
					if cmp('\xc2\xa3', betValue[:2]) == 0:
						betValue = betValue[2:]
						fp.write( "CSF %s\n" %(betValue))
					if cmp('\xe2\x82', betValue[:2]) == 0:
						betValue = betValue[3:]
						betValue = str(change_rate(float(betValue), exchangeRate))
						fp.write( "CSF %s\n" %(betValue))
				elif cmp(betItem.text, 'Trifecta:') == 0:
					betValue = betItem.findNextSibling().text.encode('utf-8')
					if cmp('\xc2\xa3', betValue[:2]) == 0:
						betValue = betValue[2:]
						fp.write( "Trifecta %s\n" %(betValue))
					if cmp('\xe2\x82', betValue[:2]) == 0:
						betValue = betValue[3:]
						betValue = str(change_rate(float(betValue), exchangeRate))
						fp.write( "Trifecta %s\n" %(betValue))					
				elif cmp(betItem.text, 'Tricast:') == 0:
					betValue = betItem.findNextSibling().text.encode('utf-8')
					if cmp('\xc2\xa3', betValue[:2]) == 0:
						betValue = betValue[2:]
						fp.write( "Tricast %s\n" %(betValue))
					if cmp('\xe2\x82', betValue[:2]) == 0:
						betValue = betValue[3:]
						betValue = str(change_rate(float(betValue), exchangeRate))
						fp.write( "Tricast %s\n" %(betValue))
fp.close
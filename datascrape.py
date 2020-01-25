# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 11:27:45 2017

@author: Ben
"""

import requests
from bs4 import BeautifulSoup
import os


total = ""  #iniitilize data entry
url = 'https://coinmarketcap.com/currencies/ethereum/historical-data/?start=20130428&end=20171118'
thepage = requests.get(url)
soupdata = BeautifulSoup(thepage.text, "html.parser")   #make data useful

for record in soupdata.findAll('tr'):   #finds table in soup
    day = ''                            #initilizes data for row
    for data in record.findAll('td'):       #loops through each column in row
        temp = unicode.encode(data.text)    #converts datatype to string
        temp = temp.replace(',','')         #gets rid of commas so it can be converted to csv
        day = day + ',' + temp              #adds data to row with comma between
    total = total + '\n' + day[1:]          #once row is complete add to next line of total

header='Date,Open,High,Low,Close,Volume,Market Cap' + '\n'  #header for csv
file=open(os.path.expanduser('ETH Hist.csv'),'wb')          #creates file for csv
file.write(bytes(header))                                   #adds header to new file
file.write(bytes(total))                                    #adds total to new file
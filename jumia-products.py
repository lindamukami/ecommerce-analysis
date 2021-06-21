# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 21:59:29 2021

@author: v-limac
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
baseurl = 'https://www.jumia.co.ke/'
header ={
    'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
productlinks=[]
 
for x in range (1,6):
    r = requests.get(f'https://www.jumia.co.ke/catalog/?q=makeup&page={x}#catalog-listing')
    
    soup = BeautifulSoup(r.content, 'lxml')
    
    productlist = soup.find_all('article',class_='prd _fb col c-prd')
   
    
    for item in productlist:
        for link in item.find_all('a',href=True):
            #print(link['href'])
            productlinks.append(baseurl +link['href'])
        
#print(len(productlinks))
#print(productlinks)        
#testlink = 'https://www.jumia.co.ke/tinkle-eyebrow-shaper-facial-hairs-razor-3-pieces-34554689.html'
itemslist = []
for link in productlinks:
    r = requests.get(link,headers =header)
    soup = BeautifulSoup(r.content, 'lxml')
    main = soup.find('main')
    
    #print(soup.find('h1', class_ = 'product-main__name').text.strip())
    name = soup.find('h1', class_ = '-fs20 -pts -pbxs').text.strip()
    rating = soup.find('div',class_='stars _s _al').text.strip()
    reviews = soup.find('a',class_='-plxs _more').text.strip()
    price = soup.find('span',class_='-b -ltr -tal -fs24').text.strip()
    brand = main.select_one('div.-pvxs a._more').text.strip()
    jumia={
           'name':name,
           'rating':rating,
           'reviews':reviews,
           'price':price,
           'brand': brand
           }
    #print(jumia['brand'])
    itemslist.append(jumia)
    
df = pd.DataFrame(itemslist)
df.to_csv('jumia-products.csv')
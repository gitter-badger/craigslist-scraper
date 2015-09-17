import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4
import numpy as np

"""Full URL = http://losangeles.craigslist.org/search/wst/sss?sort=rel&query=lego"""

BaseURL = 'http://losangeles.craigslist.org'
URL = 'http://losangeles.craigslist.org/search/wst/sss?sort=rel&query=lego'
rsp = requests.get(URL)
html = bs4(rsp.text, 'html.parser')

"""find how many listings in querry by class: row"""
legos = html.find_all('p', attrs={'class': 'row'})


"""print how many listings found"""
num_items = len(legos)
print("Number of total records found: "+str(num_items))

"""Function to find the price"""
def find_prices(rw):
    price = rw.find('span', {'class': 'price'})
    if price is not None:
        price = price.text
    else:
        price = "0"
    return price

"""MAIN: go through each listing finding price, title, link, and date listed keeping only listings $50 or less and creating a pandas dataframe"""
results = []
for i in range(num_items):
    this_lego = legos[i]
    price = find_prices(this_lego)
    title = this_lego.find('a', attrs={'class': 'hdrlnk'}).text
    link_end = this_lego.find('a', attrs={'class': 'hdrlnk'})['href']
    link = (BaseURL + link_end)
    date_time = this_lego.find('time')['title']
    if int(price.strip('$')) < 51:
        data = np.array([date_time, title, price, link])
        col_names = ['date_time', 'title', 'price', 'link']
        df_raw = pd.DataFrame(data, index=col_names)
        df=df_raw.T
        results.append(df)

"""print dataframe to a csv to view"""
results = pd.concat(results, axis=0)
print(results)
results.to_csv('Craigslist_Lego.csv')

"""Issues and wishes.
For some reason also adds listings that are NOT wst (west side of LA).
Unable to sort by date or price
Have tried several times to integrate gmail and email to send the list but still learning about those functions and how to convert the dataframe into a readable string to be added to the email body."""

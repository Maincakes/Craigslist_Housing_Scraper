from time import sleep
import re
from random import randint
from warnings import warn
from time import time
import requests
from IPython.core.display import clear_output
from bs4 import BeautifulSoup
from requests import get
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pylab as pylab
from matplotlib import figure
import matplotlib.pyplot as plt
import seaborn as sns

response = get('https://bend.craigslist.org/search/apa?availabilityMode=0&hasPic=1')
soup = BeautifulSoup(response.text, 'html.parser')

# This class 'search-legend' encompasses the entire legend bar of a craigslist postings page.
results_num = soup.find('div', class_='search-legend')
# This finds the total amount of posts and saves them as an integer.
results_total = int(results_num.find('span', class_='totalcount').text)

# We can see from the craigslist website that each page has 120 posts.
# The arrange function takes the starting value = 0, the ending value which is equal to the total number of posts and
# a step value which is 120 posts per page.
pages = np.arange(0, results_total+1, 120)

iterations = 0

# These are the empty lists that we are going to append to as we gather data.
post_date = []
post_hood = []
post_title = []
post_bedrooms = []
post_sqfts = []
post_link = []
post_prices = []

for page in pages:

    # Get a request from the page.
    response = get('https://bend.craigslist.org/search/apa?'
                   + 's='
                     + str(page)
                   + '&hasPic=1'
                     + '&availabilityMode=0')

    sleep(randint(1, 5))

    # Warn us if status code is not 200.
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    # This grabs the response and comes back with all of the html from the page.
    page_html = BeautifulSoup(response.text, 'html.parser')

    # Defining the post data.
    posts = soup.find_all('li', class_='result-row')

    # Start extracting the data for each of the empty lists that were defined earlier.
    for post in posts:

        # Since we are trying to find the difference of pricing in neighborhoods if the post doesn't list a
        # neighborhood then we don't want to add its data at all.
        if post.find('span', class_='result-hood') is not None:

            # Extract post date
            date = post.find('time', class_='result-date')['datetime']
            post_date.append(date)

            # Extract post neighborhood
            hood = post.find('span', class_='result-hood').text
            post_hood.append(hood)

            # Extract title text
            title = post.find('a', class_='result-title hdrlnk').text
            post_title.append(title)

            # Extract link
            link = post.find('a', class_='result-title hdrlnk')['href']
            post_link.append(link)

            # Extract price
            price = post.find('span', class_='result-price').text
            price = int(price.replace('$', ''))
            post_prices.append(price)

            # This checks to make sure that there is information available like bedroom count and square footage.
            if post.find('span', class_='housing') is not None:

                # If the first element is square footage because people quite often aren't listing the number of
                # bedrooms so the square footage text would come first.
                if 'ft2' in post.find('span', class_='housing').text.split()[0]:

                    # We are setting bedroom_count to nan because if ft2 comes first then there isn't a bedroom
                    # count listed but we still want a value for bedrooms for playing with the data later.
                    bedroom_count = np.nan
                    post_bedrooms.append(bedroom_count)

                    sqft = int(post.find('span', class_='housing').text.split()[0][:-3])
                    post_sqfts.append(sqft)

                elif len(post.find('span', class_='housing').text.split()) > 2:

                    # We are replacing the br and sqft with '' so that it only returns an integer.
                    housing_list = post.find('span', class_='housing').text.replace('br', '').replace('ft2', '',).split()
                    bedroom_count = housing_list[0]
                    post_bedrooms.append(bedroom_count)

                    # Extract the sqft which will be housing_list[2].
                    sqft = int(housing_list[2])
                    post_sqfts.append(sqft)

                # This takes into account posts that only have a bedroom count and no sqft value.
                elif len(post.find('span', class_='housing').text.split()) == 2:

                    bedroom_count = post.find('span', class_='housing').text.replace('br', '').split()[0]
                    post_bedrooms.append(bedroom_count)

                    # Since there is no sqft value we will set it to nan
                    sqft = np.nan
                    post_sqfts.append(sqft)

                # This else is for posts that don't have a bedroom count listed or a sqft listed.
                else:

                    bedroom_count = np.nan
                    post_bedrooms.append(bedroom_count)

                    sqft = np.nan
                    post_sqfts.append(sqft)

            # Return nan if there is no bedroom count or sqft.
            else:
                bedroom_count = np.nan
                post_bedrooms.append(bedroom_count)

                sqft = np.nan
                post_sqfts.append(sqft)

    iterations += 1

print('\n')


print('Scrape Complete')


apts = pd.DataFrame({'posted': post_date,
                     'neighborhood': post_hood,
                     'post title': post_title,
                     'number bedrooms': post_bedrooms,
                     'sqft': post_sqfts,
                     'URL': post_link,
                     'price': post_prices})

print(apts.info())
apts.head(10)

# Drop all duplicates that share the same URL we don't want to count the same houses twice.
apts = apts.drop_duplicates(subset='URL')
len(apts.drop_duplicates(subset='URL'))

# Convert the number of bedrooms into a float. np.nan is a float!
apts['number bedrooms'] = apts['number bedrooms'].apply(lambda x: float(x))

# Convert the date time string into a datetime object.
apts['posted'] = pd.to_datetime(apts['posted'])

# Look at what neighborhoods there are to look at
print(apts['neighborhood'].unique())

# Remove the parenthesis from the left and right side of the neighborhood names
apts['neighborhood'] = apts['neighborhood'].map(lambda x: x.lstrip().replace('(', '').rstrip(')'))

# Turn them all into titles
apts['neighborhood'] = apts['neighborhood'].str.title()

# Lots of places use a / as well as a , to break up city areas we will remove that and only take the first city area.
apts['neighborhood'] = apts['neighborhood'].apply(lambda x: x.split('/')[0])
apts['neighborhood'] = apts['neighborhood'].apply(lambda x: x.split(',')[0])

# remove whitespaces
apts['neighborhood'] = apts['neighborhood'].apply(lambda x: x.strip())

# Group by neighborhood.
print(apts.groupby('neighborhood').mean()['price'].sort_values())

# Save data to a csv file
apts.to_csv('apts_Seattle_Jan_19_2020.csv', index=False)

plt.figure(figsize=(15, 10))
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}

pylab.rcParams.update(params)
sns.boxplot(x='neighborhood', y='price', data=apts)
plt.xlabel("Neighborhood")
plt.xticks(rotation=75)
plt.ylabel('Price USD')
plt.title('Prices by Neighborhood - Boxplots')
plt.show()

# Note: This might not work depending on the first post's information. This is just a starting point to understand
# what is actually happening when we scrape craigslist.

# Get a request from site
from requests import get

from bs4 import BeautifulSoup

# This is loading the craigslist site with some variables such as has picture.
response = get('https://sfbay.craigslist.org/search/eby/apa?hasPic=1&availabilityMode=0')

soup = BeautifulSoup(response.text, 'html.parser')

posts = soup.findAll('li', class_='result-row')
post_one = posts[0]
post_one_price = post_one.a.text
post_one_price.strip()

post_one_time = post_one.find('time', class_='result-date')
#print(post_one_time)
post_one_datetime = post_one_time['datetime']
#print(post_one_datetime)

post_one_title = post_one.find('a', class_='result-title hdrlnk')
post_one_link = post_one_title['href']
#print(post_one_link)

#easy to grab the post title by taking the text element of the title variable
post_one_title_text = post_one_title.text
#print(post_one_title_text)

post_one_num_bedrooms = post_one.find('span', class_='housing')
post_one_num_bedrooms = post_one_num_bedrooms.text.split()[0]

post_one_sqft = post_one.find('span', class_='housing')
print(post_one_sqft.text.split()[2][:-3])

post_one_hood = post_one.find('span', class_='result-hood')
print(post_one_hood.text)


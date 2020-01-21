# build out the loop
from time import sleep
import re
from random import randint  # avoid throttling by not sending too many requests one after the other
from warnings import warn
from time import time
from IPython.core.display import clear_output
import numpy as np

# find the total number of posts to find the limit of the pagination
results_num = html_soup.find('div', class_='search-legend')
results_total = int(results_num.find('span',
                                     class_='totalcount').text)  # pulled the total count of posts as the upper bound of the pages array

# each page has 119 posts so each new page is defined as follows: s=120, s=240, s=360, and so on. So we need to step in size 120 in the np.arange function
pages = np.arange(0, results_total + 1, 120)

iterations = 0

post_timing = []
post_hoods = []
post_title_texts = []
bedroom_counts = []
sqfts = []
post_links = []
post_prices = []

for page in pages:

    # get request
    response = get("https://sfbay.craigslist.org/search/eby/apt?"
                   + "s="  # the parameter for defining the page number
                   + str(page)  # the page number in the pages array from earlier
                   + "&hasPic=1"
                   + "&availabilityMode=0")

    sleep(randint(1, 5))

    # throw warning for status codes that are not 200
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    # define the html text
    page_html = BeautifulSoup(response.text, 'html.parser')

    # define the posts
    posts = html_soup.find_all('li', class_='result-row')
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib import figure
import seaborn as sns
import csv
import pandas as pd

post_date = []
post_hood = []
post_title = []
post_bedrooms = []
post_sqfts = []
post_link = []
post_prices = []


with open('apts_Seattle_Jan_17_2020.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # This next function takes out all of the title information so that it starts looping on the data only.
    next(csv_reader)

    for line in csv_reader:
        print(line)
        post_date.append(line[0])
        post_hood.append(line[1])
        post_title.append(line[2])
        post_bedrooms.append(float(line[3]))
        post_sqfts.append(float(line[4]))
        post_link.append(line[5])
        post_prices.append(int(line[6]))

plt.figure(figsize=(10, 6))
plt.hist(post_prices, edgecolor='black')
plt.xlabel('Price')
plt.ylabel('Count')
plt.title('Distribution of Prices')
# plt.show()

params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large'}

pylab.rcParams.update(params)

plt.figure(figsize=(12, 8))
sns.scatterplot(x=post_prices, y=post_sqfts, hue=post_bedrooms, palette='summer', x_jitter=True, y_jitter=True, s=125)
plt.legend(fontsize=12)
plt.xlabel("Price", fontsize=18)
plt.ylabel("Square Footage", fontsize=18)
plt.title("Price vs. Square Footage Colored by Number of Bedrooms", fontsize=18)
plt.show()

plt.figure(figsize=(12, 8))
sns.regplot(x=post_prices, y=post_sqfts)
plt.title('Price vs. Square Footage Regression')
plt.xlabel('Price USD')
plt.ylabel('Square Feet')
plt.show()



#!/bin/bash

#EmreYbs 
#BBC News RSS Feed Reader(BBC News RSS Feed Reader.py) v.0.01: This scripts works but some improvements are needed. 
#So I'll work and try to improve it better.Feel free to contribute or make it for you.

import requests
from bs4 import BeautifulSoup
import cowsay
import time
from halo import Halo
import pandas as pd

cowsay.cow('Welcome to BBC News RSS Feed Reader\n\n')

response = requests.get('http://www.bbc.co.uk/news')
doc = BeautifulSoup(response.text, 'html.parser')
spinner = Halo(text="Scraping BBC News latest news headlines",spinner='dots')
spinner.start("\n Beginning...")
time.sleep(4)

headlines = doc.find_all('h3')

spinner.start("\nHere are the latest headlines from BBC News: \n")
time.sleep(2)
spinner.succeed("\nFinished scraping the headlines from BBC News website")
time.sleep(1)

for headline in headlines:
    print(headline.text)

links = doc.find_all('a', { 'class': 'gs-c-promo-heading' })

print ("\n\t\tHere are the URLS for the news: \n")
spinner.warn("Some URLS cannot be scraped in standard output\n\n\n")
for link in links:
    print(link.text)
    print(link['href'])

summaries = doc.find_all('p', { 'class': 'gs-c-promo-summary' })
print ("\n\t\tHere are the short summaries of the news: \n")
for summary in summaries:
    print(summary.text)

# Start with an empty list
stories_list = []
stories = doc.find_all('div', { 'class': 'gs-c-promo' })
for story in stories:
    # Create a dictionary without anything in it
    story_dict = {}
    headline = story.find('h3')
    if headline:
        story_dict['HEADLINE'] = headline.text
    link = story.find('a')
    if link:
        story_dict['URL'] = link['href']
    summary = story.find('p')
    if summary:
        story_dict['SUMMARY'] = summary.text
    # Add the dict to our list
    stories_list.append(story_dict)
print("")    
spinner.succeed("Finished scraping latest news from BBC News official website\n")
spinner.info("\n\tI will create a csv file in your Desktop")
spinner.start("\nConverting to Pandas Data Frame")
time.sleep(3)
df = pd.DataFrame(stories_list)

#In terminal this part will give error due to Pandas Data Frame. 
#But in Visual Studio or similar IDE, everthing works
df.to_csv("Desktop/bbc_latest_news.csv", index=False)
spinner.info("Saved the csv file as 'bbc_latest_news.csv' ")
spinner.succeed("Finished all tasks.\n")
spinner.stop()

print(cowsay.get_output_string('stimpy', 'EmreYbs wishes you a lovely day... Bye for now'))
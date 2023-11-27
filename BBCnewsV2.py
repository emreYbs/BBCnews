#!/usr/bin/env python3
#emreYbs
# -*- coding: utf-8 -*-
# BBC News RSS Feed Reader(BBC News RSS Feed Reader.py) v.0.02

import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import datetime
import os

sleep (0.2)
def display_banner():
    """
    Displays the banner for the BBC News RSS Feed Reader project.
    """
    banner = """
                                                                              
    //   ) )  //   ) )  //   ) )       /|    / /                              
   //___/ /  //___/ /  //             //|   / /  ___                   ___    
  / __  (   / __  (   //             // |  / / //___) ) //  / /  / / ((   ) ) 
 //    ) ) //    ) ) //             //  | / / //       //  / /  / /   \ \     
//____/ / //____/ / ((____/ /      //   |/ / ((____   ((__( (__/ / //   ) )   
                                                                              
                                                        by emreYbs
    """
    
    red_banner = "\033[31m" + banner + "\033[0m"  # Add ANSI escape sequence for red color
    
    print(red_banner)
    sleep(0.2)
    print("BBC News RSS Feed Reader\n") 

def scrape_bbc_news(url):
    """
    Scrapes the latest news headlines, URLs, and summaries from the BBC News website.

    Args:
        url (str): The URL of the BBC News website.

    Returns:
        pandas.DataFrame: A DataFrame containing the scraped data.
    """
    try:
        # Set user-agent header
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        # Make HTTP request
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse HTML
        doc = BeautifulSoup(response.text, 'html.parser')

        # Scrape headlines
        headlines = doc.find_all('h3')
        sleep (0.2)
        print("\033[34m\nHere are the latest headlines from BBC News:\033[0m")
        sleep (0.2)
        for headline in headlines:
            print(headline.text)

        # Scrape URLs
        links = doc.find_all('a', {'class': 'gs-c-promo-heading'})
        sleep (0.2)
        print("\033[32m\nHere are the URLs for the news:\033[0m")
        for link in links:
            print(link.text)
            print(link['href'])

        # Scrape summaries
        summaries = doc.find_all('p', {'class': 'gs-c-promo-summary'})
        sleep (0.1)
        print("\033[35m\nHere are the short summaries of the news:\033[0m")
        sleep (0.2)
       
        for summary in summaries:
            print(summary.text)

        # Create a list of dictionaries for each story
        stories_list = []
        stories = doc.find_all('div', {'class': 'gs-c-promo'})
        sleep (0.1)
        for story in stories:
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
            stories_list.append(story_dict)

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(stories_list)

        return df

    except requests.exceptions.RequestException as e:
        print("\033[31mAn error occurred during the scraping process:\033[0m", str(e)) 
        return None

# Display banner
display_banner()
sleep (0.2)

# Scrape BBC News
url = 'http://www.bbc.co.uk/news'
df = scrape_bbc_news(url)

if df is not None:
            # Get current date
    current_date = datetime.date.today().strftime("%Y%m%d")
    try:
        # Save the DataFrame as a CSV file
        df.to_csv("Desktop/bbc_latest_news.csv", index=False)
        #print("\033[34m\nFinished scraping latest news from BBC News official website\n\033[0m")
        print(f"\033[34m\nFinished scraping latest news from BBC News official website on {current_date}\n\033[0m")
        sleep (0.1)
     

        # Get current date
        current_date = datetime.date.today().strftime("%Y%m%d")

        try:
            # Save the DataFrame as a CSV file with the current date
            filename = f"bbc_latest_news_{current_date}.csv"
            df.to_csv(os.path.join("Desktop", filename), index=False)
            print(f"\033[32mSaved the csv file as '{filename}'\033[0m")
        except Exception as e:
            print("\033[31mAn error occurred while saving the CSV file:\033[0m", str(e))
        sleep (0.1)
    except Exception as e:
        print("\033[31mAn error occurred while saving the CSV file:\033[0m", str(e)) 

sleep (0.1)
print("\nBye for now!\n")
print("\033[34m\tExitted...\033[0m")
sleep (0.1)




"""
Books Scraper - Scrape Book price and items from http://books.toscrape.com/
"""

import requests
import time
import csv
import re

from bs4 import BeautifulSoup

def browseAndScrape(seedUrl, pageNumber=1):
    # Fetch the URL - We will be using this to append to images and info routes
    urlPat       = re.compile(r'(http://.*\.com)')
    sourceUrl    = urlPat.search(seedUrl).group(0)

   # PageNumber from the argument gets formatted in the URL & Fetched 
    formattedUrl = seedUrl.format(str(pageNumber))

    try:
        htmlText     = requests.get(formattedUrl).text

        # Prepare the soup
        soup         = BeautifulSoup(htmlText, "html.parser")
        print (f"Now Scraping - {formattedUrl}")

        # This if clause stops the script when it hits an empty page
        if soup.find('li',class_='next') != None:
            scrape(sourceUrl, soup)     # Invoke the scrape function 
            time.sleep(3)               # Be a responsible citizen by waiting before you hit again
            pageNumber+=1
            browseAndScrape(seedUrl, pageNumber) # Recursively invoke the same function with the increment
        else:
            scrape(sourceUrl, soup)     # The script exits here
            return True
        return True
    except Exception as e:
        return e

def writeToCsv(listInput):
    #The scraped info will be written to a CSV here.
    try:
        with open("allBooks.csv", "a") as fopen: #Open the csv file.
            csvWriter = csv.writer(fopen)
            csvWriter.writerow(listInput)
    except:
        return False

def scrape(sourceUrl, soup): #takes the driver and the subdomain for concats as params

    # Find the elements of the article tag
    books = soup.find_all('article', class_='product_pod')

    # Iterate over each book article tag
    for eachBook in books:
        infoUrl      = sourceUrl+'/'+eachBook.h3.find('a')['href']
        coverUrl     = sourceUrl+'/catalogue'+eachBook.a.img['src'].replace('..','')

        title        = eachBook.h3.find('a')['title']
        rating       = eachBook.find('p', class_="star-rating")['class'][1]
        # can also be written as : eachBook.h3.find('a').get('title')
        price        = eachBook.find('p', class_='price_color').text.strip().encode('ascii','ignore').decode('ascii')
        availability = eachBook.find("p", class_="instock availability").text.strip()

        writeToCsv([infoUrl,coverUrl,title,rating,price,availability]) # Invoke the writeToCsv function

if __name__ == "__main__":

    seedUrl = "http://books.toscrape.com/catalogue/page-{}.html"
    print ("Web scraping has begun")
    result = browseAndScrape(seedUrl)
    if result == True:
        print ("Web scraping is now complete!")
    else:
        print (f"Oops, That doesn't seem right!!! - {result}")
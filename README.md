# Webscraper to scrape articles using beautifulsoup in Python

A scraper to scrape information from https://books.toscrape.com/.

### Setup

```sh
# Clone the repository and setup virtual environment
git clone https://github.com/StackAbuse/parsing-html-with-beautifulsoup-in-python
cd parsing-html-with-beautifulsoup-in-python
python3 -m venv .

# Install required modules
source bin/activate
pip3 install -r requirements.txt
```

### Scraping

```sh
python3 scraper.py
```

The scraped information is available in the current working directory under the filename `allBooks.csv`.
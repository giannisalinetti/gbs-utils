import argparse
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def fetch_page(url):
    """Fetch the content of the page using selenium"""
    driver = webdriver.Remote("http://selenium:4444/wd/hub", options=webdriver.ChromeOptions())
    driver.get(url)
    content = driver.page_source
    driver.quit()
    return content

def scrape_headers(content):
    """Parse the web page and extract article titles"""
    soup = BeautifulSoup(content, 'html.parser')
    titles = []

    for title in soup.find_all(re.compile("^h[123]")):
        titles.append(title.get_text())

    return titles

def scrape_links(content):
    """Parse the web page and extract article links"""
    soup = BeautifulSoup(content, 'html.parser')
    links = []

    for link in soup.find_all('a'):
        if link.has_attr('href'):
            links.append(link['href'])

    return links

def scrape_text(content, pattern):
    """Parse the web page and extract article substrings"""
    soup = BeautifulSoup(content, 'html.parser')
    substrings = []

    for substring in soup.find_all(string=re.compile(pattern)):
        substrings.append(substring.get_text())

    return substrings

def main():
    # Set the argument parses
    parser = argparse.ArgumentParser(description="Target webpage for scraping")
    parser.add_argument('url', type=str, help='The URL of the webpage to fetch')
    parser.add_argument('--target', default='headers', choices=['headers', 'links', 'text'])
    parser.add_argument('--regex', type=str, default='', help='Regex pattern of the text search')

    # Parse the Arguments
    args = parser.parse_args()

    page_content = fetch_page(args.url)
    
    match args.target:
        case 'headers':
            page_titles = scrape_headers(page_content)
            for idx, title in enumerate(page_titles, start=1):
                print(f"{idx}. {title}")
        case 'links':
            page_links = scrape_links(page_content)
            for idx, link in enumerate(page_links, start=1):
                print(f"{idx}. {link}")
        case 'text':
            page_substrings = scrape_text(page_content, args.regex)
            for idx, substring in enumerate(page_substrings, start=1):
                print(f"{idx}. {substring}")

if __name__ == "__main__":
    main()

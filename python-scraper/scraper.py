#!/usr/bin/python

import argparse
import re
import os
import sys
import validators
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class Scraper:
    selenium_remote = "http://selenium:4444/wd/hub"

    def __init__(self, url):
        self.url = url
        self.content = None

        # Validate URL format and if reachable
        status, msg = self.__check_url()
        if not status:
            print(msg)
            sys.exit(1)
      
        # Finally fetch page content
        self.__fetch_page()
         
    def __fetch_page(self):
        """Fetch the content of the page using selenium"""
        if self.__is_container():
            driver = webdriver.Remote(selenium_remote, options=webdriver.ChromeOptions())
        else:
            driver = webdriver.Chrome()
        driver.get(self.url)
        self.content = driver.page_source
        driver.quit()

    def __is_container(self):
        """Check if the current process is running inside a container"""
        return os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')

    def __check_url(self):
        """Check if url is valid and reachable and raise exception in case of error"""
        try:
            validators.url(self.url)
        except Exception as e:
            return False, f"Invalid URL format {e}"

        try:
            response = requests.head(self.url, allow_redirects=True, timeout=10)
            if response.status_code == 200:
                return True, ""
            else:
                return False, f"URL is not reachable. Status code: {respose.status_code}"
        except requests.RequestException as e:
            return False, f"URL is not reachable. Error: {e}"


    def scrape_headers(self):
        """Parse the web page and extract article titles"""
        soup = BeautifulSoup(self.content, 'html.parser')
        titles = []

        for title in soup.find_all(re.compile("^h[123]")):
            titles.append(title.get_text())

        return titles

    def scrape_links(self):
        """Parse the web page and extract article links"""
        soup = BeautifulSoup(self.content, 'html.parser')
        links = []

        for link in soup.find_all('a'):
            if link.has_attr('href'):
                links.append(link['href'])

        return links

    def scrape_text(self, pattern):
        """Parse the web page and extract article substrings"""
        soup = BeautifulSoup(self.content, 'html.parser')
        substrings = []

        for substring in soup.find_all(string=re.compile(pattern)):
            res = substring.get_text()
            if res != "":
                substrings.append(res)

        return substrings

def main():
    # Set the argument parses
    parser = argparse.ArgumentParser(description="Target webpage for scraping")
    parser.add_argument('url', type=str, help='The URL of the webpage to fetch')
    parser.add_argument('--target', default='headers', choices=['headers', 'links', 'text'])
    parser.add_argument('--regex', type=str, default='', help='Regex pattern of the text search')

    # Parse the Arguments
    args = parser.parse_args()

    # Instantiate Scraper class
    scraper = Scraper(args.url)
    
    match args.target:
        case 'headers':
            page_titles = scraper.scrape_headers()
            for idx, title in enumerate(page_titles, start=1):
                print(f"{idx}. {title}")
        case 'links':
            page_links = scraper.scrape_links()
            for idx, link in enumerate(page_links, start=1):
                print(f"{idx}. {link}")
        case 'text':
            page_substrings = scraper.scrape_text(args.regex)
            for idx, substring in enumerate(page_substrings, start=1):
                print(f"{idx}. {substring}")

if __name__ == "__main__":
    main()

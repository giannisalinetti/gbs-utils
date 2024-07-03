# Web scraper utility

## Instructions
Install prerequisites
```
$ pip install selenium beautifulsoup4
```

To scrape headers:
```
$ python scraper.py --target headers http://www.example.com
```

To scrape links:
```
$ python scraper.py --target links http://www.example.com
```

To scrape text using regular expressions:
```
$ python scraper.py --target text --regex '[eE]exam.*' http://www.example.com
```

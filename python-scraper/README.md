# Web scraper utility

## Instructions for local execution
Install prerequisites
```
$ pip install selenium beautifulsoup4 validators requests
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

This containerized version uses a containeried version of selenium-chrome to query the
target website. 

## Instructions for containerized execution

Build the container image 
```
$ podman build -t scraper .
```

Run the compose file to start the selenium-chrome service on port 4444
```
$ podman-compose up -d
```

Run the scraper container passing the arbitrary arguments
```
$ podman run scraper --target headers https://www.example.com 
```

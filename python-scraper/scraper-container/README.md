# Containerized scraper
This containerized version uses a containeried version of selenium-chrome to query the
target website. 

## Instructions
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

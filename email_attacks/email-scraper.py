from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

user_url = str(input('[+] Enter target URL to scan: '))
urls = deque([user_url])


scraped_urls = set()
emails = set()

count = 0

try:
    while len(urls):
        count +=1
        if count == 100:
            break
        url = urls.popleft()
        scraped_urls.add(url)
        

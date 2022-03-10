from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

# https://www.kea.dk

ting = 0


def update_output_text(window, field_to_update, new_text):
    window[field_to_update].update(new_text)
    window.refresh()


def stop_scrape():
    global ting
    ting += 1


def reset_scrape_flag():
    global ting
    ting = 0


def scrape_emails(target, window):
    scraped_urls = set()
    emails = set()
    count = 0
    output = ''
    web_prefix = 'https://www.'
    sub_domains = []
    urls = deque([str(web_prefix + target)])
    out_string = ''
    global ting

    # update_output_text(window=window, field_to_update='-OUTPUT-', new_text='')
    try:
        output = ''
        while len(urls):
            count += 1
            global ting
            if count == 100:
                break
            elif ting > 0:
                break
            print(ting)
            url = urls.popleft()
            scraped_urls.add(url)

            parts = urllib.parse.urlsplit(url)
            base_url = '{0.scheme}://{0.netloc}'.format(parts)

            path = url[:url.rfind('/') + 1] if '/' in parts.path else url
            out_string += '\n [%d] Processing %s' % (count, url)
            sub_domains.append([re.findall(r"[a-z0-9\.\-+_]+.[a-z0-9\.\-+_]+\.[a-z]+.[a-z0-0\.\-+_']", url)])
            output += url + '\n'
            # NOTE TO SELF: CAN BE EXTENDED TO PRINT SUBDOMAINS WITHOUT TLS/SSL
            #   update_output_text(window=window, field_to_update='-OUTPUT-', new_text=output)
            # print('[%d] Processing %s' % (self.count, url))

            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
            emails.update(new_emails)

            soup = BeautifulSoup(response.text, features="lxml")

            for anchor in soup.find_all("a"):
                link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                elif link not in urls and link not in scraped_urls:
                    urls.append(link)

    except KeyboardInterrupt:
        print('[-] Closing!')

    for mail in emails:
        output += mail + '\n'
    # update_output_text(window=window, field_to_update='-OUTPUT-', new_text=output)
    #  print(mail)
    print('\nDONE')
    print(ting)

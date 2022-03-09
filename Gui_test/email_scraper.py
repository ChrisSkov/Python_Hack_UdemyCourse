from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
import main as ting

# https://www.kea.dk

ui_ting = ting.UITing()


def update_output_text(window, field_to_update, new_text):
    window[field_to_update].update(new_text)
    window.refresh()


class EmailScraper:
    scraped_urls = set()
    emails = set()
    urls = ''
    count = 0

    def scrape_emails(self, target, window):
        web_prefix = 'https://www.'
        sub_domains = []
        self.urls = deque([str(web_prefix + target)])
        out_string = ''
        try:
            while len(self.urls):
                self.count += 1
                if self.count == 100:
                    break
                url = self.urls.popleft()
                self.scraped_urls.add(url)

                parts = urllib.parse.urlsplit(url)
                base_url = '{0.scheme}://{0.netloc}'.format(parts)

                path = url[:url.rfind('/') + 1] if '/' in parts.path else url
                out_string += '\n [%d] Processing %s' % (self.count, url)
                sub_domains.append([re.findall(r"[a-z0-9\.\-+_]+.[a-z0-9\.\-+_]+\.[a-z]+.[a-z0-0\.\-+_']", url)])
                update_output_text(window=window, field_to_update='-OUTPUT-', new_text=sub_domains)
                print('[%d] Processing %s' % (self.count, url))

                try:
                    response = requests.get(url)
                except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                    continue

                new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
                self.emails.update(new_emails)

                soup = BeautifulSoup(response.text, features="lxml")

                for anchor in soup.find_all("a"):
                    link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                    if link.startswith('/'):
                        link = base_url + link
                    elif not link.startswith('http'):
                        link = path + link
                    elif link not in self.urls and link not in self.scraped_urls:
                        self.urls.append(link)

        except KeyboardInterrupt:
            print('[-] Closing!')

        for mail in self.emails:
            out_string += '\n '
            out_string += mail
            update_output_text(window=window, field_to_update='-OUTPUT-', new_text=out_string)
            print(mail)


if __name__ == '__main__':
    es = EmailScraper()
    es.scrape_emails('https://www.kea.dk')

from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
import main as ting

# https://www.kea.dk

ui_ting = ting.UILayout()


def update_output_text(window, field_to_update, new_text):
    window[field_to_update].update(new_text)
    window.refresh()


class EmailScraper:

    def scrape_emails(self, target, window):
        scraped_urls = set()
        emails = set()
        urls = ''
        count = 0
        output = ''
        web_prefix = 'https://www.'
        sub_domains = []
        urls = deque([str(web_prefix + target)])
        out_string = ''
        update_output_text(window=window, field_to_update='-OUTPUT-', new_text='')
        try:
            output = ''
            while len(urls):
                count += 1
                if count == 10:
                    break
                url = urls.popleft()
                scraped_urls.add(url)

                parts = urllib.parse.urlsplit(url)
                base_url = '{0.scheme}://{0.netloc}'.format(parts)

                path = url[:url.rfind('/') + 1] if '/' in parts.path else url
                out_string += '\n [%d] Processing %s' % (count, url)
                sub_domains.append([re.findall(r"[a-z0-9\.\-+_]+.[a-z0-9\.\-+_]+\.[a-z]+.[a-z0-0\.\-+_']", url)])
                output += url + '\n'
                # NOTE TO SELF: CAN BE EXTENDED TO PRINT SUBDOMAINS WITHOUT TLS/SSL
                update_output_text(window=window, field_to_update='-OUTPUT-', new_text=output)
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
            update_output_text(window=window, field_to_update='-OUTPUT-', new_text=output)
            print(mail)
        print('\nDONE')


if __name__ == '__main__':
    es = EmailScraper()
    es.scrape_emails('https://www.kea.dk')

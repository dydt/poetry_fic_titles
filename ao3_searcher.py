import BeautifulSoup as bs
import csv
import requests
import re
import time

def search_fics(string):
    # TODO: Add info to user-agent
    resp = requests.get('http://archiveofourown.org/works/search',
                        params = {'work_search[title]': "\"" + string + "\""})
    return resp.text

def parse_results(html):
    soup = bs.BeautifulSoup(html)

    heading = soup.find('h3', {"class": "heading"})

    try: # What if there are no results?
        heading_text = heading.getText()
    except AttributeError:
        return 0, []

    num_found = re.match(r'(?P<number>\d+)', heading_text)
    num_results = num_found.group('number')

    fandoms_classes = soup.findAll('h5', {"class": "fandoms heading"})
    fandoms = set([link.a.text for link in fandoms_classes])

    return num_results, list(fandoms)

if __name__ == '__main__':
    titles = [x.strip('\n') for x in open('viable_grams.txt').readlines()]

    with open('titles_counts_fandoms.csv', 'a') as results:
        writer = csv.DictWriter(results, ['title', 'num_results', 'fandoms'])
        writer.writeheader()

        for title in titles:
            num_found, fandoms = parse_results(search_fics(title))
            writer.writerow({'title': title,
                         'num_results': num_found,
                         'fandoms': str(fandoms)})
            time.sleep(5)

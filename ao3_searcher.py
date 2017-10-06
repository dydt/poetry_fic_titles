import BeautifulSoup as bs
import requests 
import re

def search_fics(string):
    # TODO: Add info to user-agent
    resp = requests.get('http://archiveofourown.org/works/search',
                        params = {'work_search[title]': string})
    return resp.text

def parse_results(html):
    soup = bs.BeautifulSoup(html)

    heading = soup.find('h3', {"class": "heading"})
    num_found = re.match(r'(?P<number>\d+)', heading.getText())
    num_results = num_found.group('number')

    fandoms_classes = soup.findAll('h5', {"class": "fandoms heading"})
    fandoms = set([link.a.text for link in ])

    return num_results, fandoms

if __name__ == '__main__':
    possible_titles = open('viable_ngrams.txt').readlines()
    with open('titles_counts_fandoms.csv', 'a') as results:
        writer = csv.DictWriter(results, ['title', 'num_results', 'fandoms'])
        writer.writeheader()

        for title in possible_titles:
            num_found, fandoms = parse_results(search_fics(title))
            writer.write{'title': title,
                         'num_results': num_found,
                         'fandoms': str(fandoms)}
            sleep(10)

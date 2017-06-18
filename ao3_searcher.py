import BeautifulSoup as bs
import requests 
import re

def find_fics(string):
	# TODO: Add info to user-agent
	resp = requests.get('http://archiveofourown.org/works/search',
						params = {'work_search[title]': string})
	return resp.text

def parse_results(html):
	soup = bs.BeautifulSoup(html)

	heading = soup.find('h3', {"class": "heading"})
	num_found = re.match(r'(?P<number>\d+)', heading.getText())
	num_results = num_found.group('number')

	return num_results

if __name__ == '__main__':
	print parse_results(find_fics('landscape after cruelty'))
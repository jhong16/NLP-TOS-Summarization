import certifi
import urllib3
import json
import logging
from bs4 import BeautifulSoup
from argparse import ArgumentParser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HTTP = urllib3.PoolManager()


parser = ArgumentParser()
parser.add_argument('--link_file', '-l',
    help="""
        JSON file containing links to TOS pages that should be parsed.
        JSON file should be structured as follows:
        {<COMPANY_NAME>: { <DOCUMENT_TYPE>: <DOCUMENT_URL> } }.
        <DOCUMENT_TYPE> can be
    """)
parser.add_argument('--output_file', '-o',
    help='File to which output should be written.')

args = parser.parse_args()

assert args.link_file is not None
assert args.output_file is not None

with open(args.link_file, 'r') as fp:
    companies = json.load(fp)

web_data = {}
for company in companies:
    web_data[company] = {}
    for name, url in companies[company].items():
        if name.lower() == "terms of service":
            print('Connecting to {url}'.format(url=url))
            try:
                res = HTTP.request('GET', url)
                soup = BeautifulSoup(res.data, 'html.parser')

                # keep list elements since they might be in code of conduct and negated.
                list_elems = soup.find_all('li')
                for i, elem in enumerate(list_elems):
                    list_elems[i].replace_with("---" + elem.text)
                # kill all script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()    # rip it out
                # remove header tags, though they could be interesting for classification
                for header in soup(["h1", "h2", "h3"]):
                    header.decompose()

                # get text
                text = soup.get_text()

                # break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())
                # break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # drop blank lines
                # text = '\n'.join(chunk for chunk in chunks if chunk)
                
                web_data[company][url] = text
                    
            except urllib3.exceptions.RequestError as e:
                print(e)

with open(args.output_file, "w") as fp:
    json.dump(web_data, fp)

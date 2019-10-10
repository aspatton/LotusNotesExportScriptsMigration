import re
import requests
from bs4 import BeautifulSoup
import csv

baseURL = "http://www.avajava.com/tutorials/lessons/"
with open("export.csv") as sourceFile:
    csv_reader = csv.reader(sourceFile, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count = line_count + 1
        else:
            line_count = line_count + 1
            print(f'\t{row[0]} and {row[1]}')
        pageURL = baseURL + str(row[1])
        response = requests.get(str(pageURL))
        response.raw.decode_content = True
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        urls = [img['src'] for img in img_tags]
        for url in urls:
            filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
            with open(filename.group(1), 'wb') as f:
                if 'http' not in url:
                    url = '{}{}'.format(pageURL, url)
                response = requests.get(url)
                f.write(response.content)

import re
import requests
from bs4 import BeautifulSoup
import csv
import os
import sys

dominoURL = "your Domino URL"
# Directory to save images that were embedded in Notes docs
embedDir = "Embedded"
# Complete local path
baseDir = "C:\\Users\\Installer\\notesexporttest\\Embedded\\"
# First command line argument specifies import file
if (len(sys.argv) > 1):
	importFile = sys.argv[1]
else:
	importFile = "export.csv"
# Second command line argument specifies output file
if (len(sys.argv) > 2):
	exportFile = sys.argv[2]
else:
	exportFile = "newexport.csv"
# Third command line argument specifies Domino base URL
if (len(sys.argv) > 3):
	parentPath = sys.argv[3]
else:
	parentPath = dominoURL
# The fourth command line argument specifies Domino view URL
if (len(sys.argv) > 4):
	baseURL = sys.argv[4]
else:
	baseURL = "test or standard url to be used"

endURL = "?OpenDocument"

with open(importFile) as sourceFile:
	csv_reader = csv.reader(sourceFile, delimiter=',')
	line_count = 0
	c=0
	for row in csv_reader:
		print(f'\t{line_count} - {row[0]} and {row[1]}')
		if line_count > 0:
			docID = row[0]
			pageURL = baseURL + docID + endURL
			username = 'username'
			password = 'password'
			response=requests.get(pageURL,auth=(username, password))
			response.raw.decode_content = True
			soup = BeautifulSoup(response.text, 'html.parser')
			img_tags = soup.find_all('img')
			urls = [img['src'] for img in img_tags]
			c=0
			if urls:
				embedded = []
				for url in urls:
					# search for path to embedded images
					filename = re.search('\/bbuilder\/[a-zA-Z0-9.\/?]*OpenElement',url)

					if filename:
						if filename.group():
							filename2 = "Embedded\\" + docID + "_" + str(c) + ".gif"
							c = c + 1
							with open(filename2,'wb') as f:
								url = filename.group()
								if 'http' not in url:
									url = '{}{}'.format(parentPath, url)
								print(url)
								response = requests.get(url,auth=(username, password))
								f.write(response.content)
								f.close()
								if (os.path.exists(filename2)):
									if (os.path.getsize(filename2) > 5000):
										row.append(filename2)
									else:
										os.remove(filename2)
		line_count = line_count + 1
		writer = csv.writer(open(exportFile, 'a'),delimiter=',', lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(row)						

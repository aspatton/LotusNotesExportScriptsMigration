import re
import requests
from bs4 import BeautifulSoup
import csv
import os
import sys
from slugify import slugify

embedDir = "Embedded"
baseDir = "C:\\Users\\Installer\\notesexporttest\\Embedded\\"
baseSaveDir = "C:\\Users\\Installer\\notesexporttest\\"
# First command line argument specifies import file
if (len(sys.argv) > 1):
	importFile = sys.argv[1]
else:
	importFile = "export250.csv"
# Second command line argument specifies output file
if (len(sys.argv) > 2):
	exportFile = sys.argv[2]
else:
	exportFile = "newexport.csv"
# Third command line argument specifies Domino base URL
if (len(sys.argv) > 3):
	parentPath = sys.argv[3]
else:
	parentPath = "http://domino1.1800extrude.com"
# The fourth command line argument specifies Domino view URL
if (len(sys.argv) > 4):
	baseURL = sys.argv[4]
else:
	baseURL = "http://domino1.1800extrude.com/bbuilder/manufkb.nsf/(David%20Export%20View)/"
#importFile = "export200.csv"
#parentPath = "http://domino1.1800extrude.com"
#baseURL = "http://domino1.1800extrude.com/bbuilder/manufkb.nsf/(David%20Export%20View)/"
#baseURL = parentPath + "/bbuilder/manufkb.nsf/(David%20Export%20View)/"
endURL = "?OpenDocument"
#baseURL = "http://domino1.1800extrude.com/bbuilder/manufkb.nsf/b18dde32cf58181885256444000dc6a8/be8e13eb6c4d6dc7852575f3004606f5"
with open(importFile) as sourceFile:
	csv_reader = csv.reader(sourceFile, delimiter=',')
	line_count = 0
	for row in csv_reader:
		print(f'\t{line_count} - {row[0]} and {row[1]}')
		if line_count > 0:
			docID = row[0]
			pageURL = baseURL + docID + endURL
			username = 'David Kidd'
			password = 'Install2008'
			#print(pageURL)
			response=requests.get(pageURL,auth=(username, password))
			response.raw.decode_content = True
			soup = BeautifulSoup(response.text, 'html.parser')
			img_tags = soup.find_all('img')
			#print(img_tags)
			urls = [img['src'] for img in img_tags]
			c=0
			if urls:
				embedded = []
				for url in urls:
					#print(url)
					filename = re.search('\/bbuilder\/[a-zA-Z0-9.\/?]*OpenElement',url)

					if filename:
						if filename.group():
							#print('1')
							filename2 = "Embedded\\" + docID + "_" + str(c) + ".gif"
							#c = c + 1
							with open(filename2,'wb') as f:
								url = filename.group()
								if 'http' not in url:
									url = '{}{}'.format(parentPath, url)
								print(url)
								response = requests.get(url,auth=(username, password))
								f.write(response.content)
								f.close()
								s = filename2
								clean_basename=slugify(os.path.splitext(s)[0])
								clean_extension=slugify(os.path.splitext(s)[1][1:])
								if (clean_extension):

									clean_filename='{}.{}'.format(clean_basename,clean_extension)
								elif clean_basename:

									clean_filename=clean_basename

								else:

									clean_filename = 'none'
								filename2 = clean_filename
								if (os.path.exists(filename2)):
									if (os.path.getsize(filename2) > 5000):
										c=c+1
										#row[15}=filename2
										row.insert(c+15, baseSaveDir + filename2)
									else:
										os.remove(filename2)
		line_count = line_count + 1
		writer = csv.writer(open(exportFile, 'a'),delimiter=',', lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(row)						
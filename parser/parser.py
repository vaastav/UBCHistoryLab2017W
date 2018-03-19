import csv
import sys
import re
import os
from urllib.request import urlopen
from urllib.error import HTTPError

def get_urls(filename):
    urls = []
    with open(filename, 'r+') as f:
        reader = csv.DictReader(f)
        for row in reader:
            urls += [row['TxtURL']]
    return urls

def save_files(urls):
    for url in urls:
        name = re.search('https?\:\/\/chroniclingamerica\.loc\.gov\/lccn\/(.*)', url, re.IGNORECASE)
        if name:
            filename = name.group(1)
            filename = filename.replace('/', '_')
        filename = os.path.join('./raw_data', filename)
        if os.path.isfile(filename):
            continue
        try:
            response = urlopen(url)
            data = response.read()
        except HTTPError:
            print("Failed to get : " + url)
            continue
        with open(filename, 'wb+') as f:
            f.write(data)

def usage():
    print("Usage : python parser.py <csv_file_with_urls>")
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        usage()
    urls = get_urls(sys.argv[1])
    print(len(urls))
    save_files(urls)

if __name__ == '__main__':
    main()

import csv
import sys
import re
import os
from urllib.request import urlopen
from urllib.error import HTTPError

regex_urls = {
    "ChroniclingAmerica" : "https?\:\/\/chroniclingamerica\.loc\.gov\/lccn\/(.*)",
    "BC" : "https?\:\/\/open\.library\.ubc\.ca\/media\/download\/full-text\/(.*)",
    "Oregon" : "https?\:\/\/oregonnews\.uoregon\.edu\/lccn\/(.*)",
    "NewYork" : "https?\:\/\/nyshistoricnewspapers.org\/lccn\/(.*)",
    "Newspaper" : ""
}

def get_urls(filename):
    urls = []
    with open(filename, 'r+') as f:
        reader = csv.DictReader(f)
        print(reader.fieldnames)
        for row in reader:
            urls += [row['TxtURL']]
    return urls

def get_regex(source):
    print(source)
    return regex_urls[source]

def save_files(urls, source):
    regex = get_regex(source)
    out_dir = "./raw_data_" + source
    for url in urls:
        name = re.search(regex, url, re.IGNORECASE)
        if name:
            filename = name.group(1)
            filename = filename.replace('/', '_')
        filename = os.path.join(out_dir, filename.strip())
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
    print("Usage : python parser.py <csv_file_with_urls> <source>")
    sys.exit(1)

def main():
    if len(sys.argv) != 3:
        usage()
    urls = get_urls(sys.argv[1])
    print(len(urls))
    source = sys.argv[2]
    #print(get_regex(source))
    save_files(urls, source)

if __name__ == '__main__':
    main()

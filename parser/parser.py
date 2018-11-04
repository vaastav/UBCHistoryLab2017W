import csv
import sys
import re
import os
from urllib.request import urlopen
from urllib.error import HTTPError
from html.parser import HTMLParser

class NewspaperHTMLParser(HTMLParser):
    should_get_data = False
    data = ""
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            for a in attrs:
                if a[0] == "itemprop" and a[1] == "content":
                    self.should_get_data = True

    def handle_endtag(self, tag):
        if self.should_get_data:
            self.should_get_data = False

    def handle_data(self, data):
        if self.should_get_data:
            self.data += data

regex_urls = {
    "ChroniclingAmerica" : "https?\:\/\/chroniclingamerica\.loc\.gov\/lccn\/(.*)",
    "BC" : "https?\:\/\/open\.library\.ubc\.ca\/media\/download\/full-text\/(.*)",
    "Oregon" : "https?\:\/\/oregonnews\.uoregon\.edu\/lccn\/(.*)",
    "NewYork" : "https?\:\/\/nyshistoricnewspapers\.org\/lccn\/(.*)",
    "Georgia" : "https?\:\/\/gahistoricnewspapers\.galileo\.usg\.edu\/lccn/(.*)",
    "Newspaper" : "https?\:\/\/www\.newspapers\.com\/newspage\/(.*)\/"
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

def parse_newspaper_com_links(urls):
    out_dir = "./raw_data_Newspaper"
    regex = get_regex("Newspaper")
    for url in urls:
        name = re.search(regex, url, re.IGNORECASE)
        if name:
            filename = name.group(1)
            filename = filename.replace('/', '_')
        filename = os.path.join(out_dir, filename.strip() + ".txt")
        if os.path.isfile(filename):
            continue
        try:
            response = urlopen(url)
            data = response.read().decode("utf-8")
        except HTTPError:
            print("Failed to get : " + url)
            continue
        parser = NewspaperHTMLParser()
        parser.feed(data)
        with open(filename, 'w+', encoding="utf-8") as f:
            f.write(parser.data)

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
    if source == "Newspaper":
        parse_newspaper_com_links(urls)
    else:
        save_files(urls, source)

if __name__ == '__main__':
    main()

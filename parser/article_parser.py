import sys
import os

# Other value would be 2017W2
HISTORY_LAB_TERM = "2018W1"

def get_published_year(s):
    '''
    Returns the year the full document was published
    '''
    arr = s.split('_')
    date = arr[1]
    year = date.split('-')[0]
    return int(year)

def num_letters(s):
    '''
    Counts the number of letters in a given string
    '''
    num = 0
    for c in s:
        if c.isalpha():
            num += 1
    return num

# Borrowed from https://stackoverflow.com/questions/2460177/edit-distance-in-python
def levenshteinDistance(s1, s2):
    '''
    Calculates the levenshtein distance between the 2 given strings
    '''
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def get_keywords(filename):
    keyword1 = ""
    keyword2 = ""
    if HISTORY_LAB_TERM == "2018W1":
        keyword1 = "pelee"
        keyword2 = "eruption"
    elif HISTORY_LAB_TERM == "2017W2":
        year = get_published_year(filename)
        keyword2 = "message"
        keyword1 = "president"
        if year >= 1877 and year <= 1880:
            keyword1 = "annual"        
    return keyword1, keyword2

def get_article(filename, dir, keyword1, keyword2):
    #keyword1, keyword2 = get_keywords(filename)

    MIN_ARTLEN = 50           # Minimum length of an article before starting a new one
    MIN_CAPSLEN = 3           # Minimum number of capital letters in a word to be considered a headline
    MAX_DIFFLEN = 5           # Maximum difference in word lengths to be compared to edit distance
    MAX_EDITDIST = 3          # Maximum edit distance between words to be considered a misspelling
    MAX_ARTLEN = 200          # Maximum length of an article before starting a new one

    # First parse to only find articles with the words president or annual
    full_filename = os.path.join(dir, filename)
    fi = open(full_filename, "r", encoding="utf8")
    try:
        contents = fi.read()
    except:
        fi.close()
        print("READ FAIL " + filename)
        return
    fi.close()
    words = contents.split()
    article = []
    articles = []
    alen = 0
    valid = False
    for word in words:
        if alen > MIN_ARTLEN and word.isupper() and num_letters(word) > MIN_CAPSLEN:
            alen = 0
            if valid:
                articles.append(article)
                article = []
                valid = False
        if abs(len(word) - len(keyword1)) < MAX_DIFFLEN and levenshteinDistance(word.lower(), keyword1) < MAX_EDITDIST:
            valid = True
        article.append(word)
        alen += 1
    # Don't forget to check the last one:
    if valid:
        articles.append(article)

    # 2nd round of filtering
    new_articles = []
    if keyword2 != "":
        for a in articles:
            valid = False
            for word in a:
                if levenshteinDistance(word.lower(), keyword2) < MAX_EDITDIST:
                    valid = True
            if valid:
                new_articles.append(a)
    else:
        new_articles = articles

    output_dir = "./output_" + dir + "/"
    
    if len(new_articles) == 0: 
        print(filename)
    else:
        output_file = output_dir + filename
        fo = open(output_file, "w+", encoding="utf8")
        for a in new_articles:
            for w in a:
                fo.write(w)
                fo.write(" ")
            fo.write("\n\n")

def get_articles(dir, kw1, kw2):
    for root, dirs, files in os.walk(dir):
        print("Num files : " + str(len(files)))
        for f in files:
            get_article(f, dir, kw1, kw2)

def usage():
    print("Usage : python article_parser.py <folder_with_txt_files> keyword1 [keyword2]")
    sys.exit(1)

def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        usage()
    dir = sys.argv[1]
    kw1 = sys.argv[2]
    kw2 = ""
    if len(sys.argv) == 4:
        kw2 = sys.argv[3]
    get_articles(dir, kw1, kw2)
    

if __name__ == '__main__':
    main()
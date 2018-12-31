# UBC HistoryLab

This reposiotry contains all the code required to download all newspapers from a csv file
and then filter the content from the sources to filter the articles out based on keywords.

## Sources Supported

Currently the following newspaper sources are supported:

+ "ChroniclingAmerica" : chroniclingamerica.loc.gov
+ "BC" : open.library.ubc.ca
+ "Oregon" : oregonnews.uoregon.edu
+ "NewYork" : nyshistoricnewspapers.org
+ "Georgia" : gahistoricnewspapers.galileo.usg.edu
+ "Newspaper" : newspaper.com 

## Downloading full articles

To download the articles from any specific source, you need a csv file that has only 1 column with the header TxtURL from that source.
Let us assume that the file is called Links_BC.csv

Create an empty folder called raw_data_[Source_Name]. For eg: to download newspapers from BC you would need to create the
empty folder called raw_data_BC.

In the parser folder, use the parser.py file to download the newspapers

```
> python parser.py <csv_file_with_links> <source>
```

## Filtering articles with keywords

To filter the articles, we need to first create an empty folder with the same name as the raw data except with the prefix "output_".

Next we need to use the script article_parser.py with the keywords to filter the articles.


## Full Example

Here is a full example of downloading and parsing articles where you are trying to download the links in Links.csv file from source BC
to find articles with keywords hello and world. The 2nd keyword is optional.

```
> mkdir raw_data_BC
> python parser.py Links.csv BC
> mkdir output_raw_data_BC
> python article_parser.py output_raw_data_BC hello world
```

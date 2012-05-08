# Fancy Matcher 1.0 - Sebastian Oehlschläger, Torsten Kunz

import csv
import sys
import difflib
from datetime import datetime
 
 
### write to csv
 
def write_to_csv(x):
     with open('searchphrases_matching.csv', 'a', newline='', encoding='latin-1') as f:
        csvwriter = csv.writer(f, delimiter=';')
        csvwriter.writerows(x)
 
### input files
 
to_match_csv = 'suchphrasen.csv'
lookup_csv = 'check_db.csv'
 
### create lookup_dict and searchword_list from input csv files
 
def create_dictionary_from_csv(csvfile):
     reader = csv.reader(open(csvfile, encoding='latin-1'), delimiter=';')
     lookup_dict = {}
     for line in reader:
          key_value = {line[1]:[line[2],line[0]]}
          if line[1] in lookup_dict and line[2] in lookup_dict[line[1]][0]:
               lookup_dict[line[1]].append(line[0])
          else:
               key_value = {line[1]:[line[2],line[0]]}
               lookup_dict.update(key_value)
#          print(lookup_dict)
     return lookup_dict

###          print(lookup_dict)
##     return lookup_dict
 
def create_searchword_list(csvfile):
     reader = csv.reader(open(csvfile, encoding='latin-1'), delimiter=';')
     searchword_list = []
     for line in reader:
          split_phrase = []
          split_phrase = [str.split(line[0])]
          split_phrase.append(line[1])
          searchword_list.append(split_phrase)
#          print(searchword_list)
     return searchword_list

###  fuzzy string comparison
 
##def string_comparison(search, lookup):
##     match_dict = {}
##     for searchword in search:
##          for key, value in lookup.items():
##               match_ratio = difflib.SequenceMatcher(None, searchword[0], key).ratio()
##               if match_ratio > 0.9:
##                    key_value = {searchword[0]:match_ratio}
##                    match_dict.update(key_value)
##          return match_dict

### vlookup

def vlookup(lookup_list, lookup_dictionary):
     for searchphrase in lookup_list:
          output = []
          for searchword in searchphrase[0]:
               if searchword in lookup_dictionary:
                    for brand in searchphrase[0]:
                         if brand in lookup_dictionary[searchword]:
                              output = []
                              output.append([searchphrase[0], searchphrase[1], searchword, brand, lookup_dictionary[searchword]])
                              write_to_csv(output)
               else:
                    x = 5                 

start = datetime.now()
lookup_dict = create_dictionary_from_csv(lookup_csv)
searchword_list = create_searchword_list(to_match_csv)
vlookup(searchword_list, lookup_dict)
stop = datetime.now()
result = stop - start
print(result)


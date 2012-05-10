# Fancy Matcher 1.3 - Sebastian Oehlschläger, Torsten Kunz

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

##def vlookup(lookup_list, lookup_dictionary):
##     print(lookup_dictionary)
##     for searchphrase in lookup_list:
##          output = []
##          for searchword in searchphrase[0]:
##               # print("searchword: " + searchword)
##               for key, value in lookup_dictionary.items():
##                    if searchword in key:
##                         for brand in searchphrase[0]:
##                              if brand in value[0]:
##                                   # print("MATCH: " + brand + " " + searchword)
##                                   output = []
##                                   output.append([searchphrase[0], searchphrase[1], searchword, brand, value])
##                                   write_to_csv(output)
##                    else:
##                         x = 5                 


## vlookup incl. string comparison

def vlookup_similar(lookup_list, lookup_dictionary):
#     print(lookup_dictionary)
     for searchphrase in lookup_list:
          for searchword in searchphrase[0]:
#               print(searchphrase, searchword)
               for key, value in lookup_dictionary.items():
#                    print(searchphrase, searchword, key, value)
                    #### Variante 1: Searchword vs. Whole Product Name
                    # name_match_ratio = difflib.SequenceMatcher(None, searchword, key).ratio()
                    # print("Search: " + searchword + " | Key: " +  key + " | Ratio = " + str(name_match_ratio))
                    # if name_match_ratio > 0.4:
                    #### Variante 2: Whole Product Name contains Searchword
                    # if searchword in key:
                    #### Variante 3: Searchword vs. each word of Product Name
                    split_name = []
                    split_name = str.split(key)
                    for partial_name in split_name:
                         name_match_ratio = difflib.SequenceMatcher(None, searchword, partial_name).ratio()
                         if name_match_ratio > 0.75:
                         ### Ende Variante 3
                              for brand in searchphrase[0]:
                                   split_brand = []
                                   split_brand = str.split(value[0])
                                   for partial_brand in split_brand:
                                        brand_match_ratio = difflib.SequenceMatcher(None, brand, partial_brand).ratio()
                                        # print("Search: " + searchword + " | Key: " +  key + " | Ratio = " + str(match_ratio))
                                        if brand_match_ratio > 0.75:
                                             # print("MATCH: " + brand + " " + searchword)
                                             for sku in value[1:]:
                                                  whole_phrase = ' '.join(searchphrase[0])
                                                  output = [[sku, whole_phrase, searchphrase[1], key, value[0], name_match_ratio, brand_match_ratio]]
                                                  write_to_csv(output)
                                        else:
                                             x = 5                 


start = datetime.now()
lookup_dict = create_dictionary_from_csv(lookup_csv)
searchword_list = create_searchword_list(to_match_csv)
vlookup_similar(searchword_list, lookup_dict)
stop = datetime.now()
result = stop - start
print(result)
# Fancy Matcher 2.1 - Sebastian Oehlschläger, Torsten Kunz

import csv
import sys
import difflib
from datetime import datetime
 
 
### write to csv
 
def write_to_csv(target_file, output):
     with open(target_file, 'w', newline='', encoding='latin-1') as f:
        csvwriter = csv.writer(f, delimiter=';')
        csvwriter.writerows(output)
 
### input files
 
to_match_csv = 'suchphrasen.csv'
lookup_csv = 'check_db.csv'
 
### create lookup_dict and searchword_list from input csv files
 
def create_dictionary_from_csv(csvfile):
     reader = csv.reader(open(csvfile, encoding='latin-1'), delimiter=';')
     lookup_dict = {}
     for line in reader:
          key_value = {line[1]:[line[2],line[3],line[0]]}
          if line[1] in lookup_dict and line[2] in lookup_dict[line[1]][0]:
               lookup_dict[line[1]].append(line[0])
          else:
               key_value = {line[1]:[line[2],line[3],line[0]]}
               lookup_dict.update(key_value)
     return lookup_dict
 
def create_searchword_list(csvfile):
     reader = csv.reader(open(csvfile, encoding='latin-1'), delimiter=';')
     searchword_list = []
     for line in reader:
          split_phrase = []
          split_phrase = [str.split(line[0])]
          split_phrase.append(line[1])
          searchword_list.append(split_phrase)
     return searchword_list

def searchword_searchphrase_dict(csvfile):
     # add search volume as [1]
     reader = csv.reader(open(csvfile, encoding='latin-1'), delimiter=';')
     input_list = []
     for line in reader:
          searchword_searchphrase_dict = {}
          split_searchphrase = str.split(line[0])
          for searchword in split_searchphrase:          
               searchword_searchphrase_dict.update({searchword:[]})
          input_list.append([searchword_searchphrase_dict, line[1]])
     return(input_list)

def vlookup_similar(lookup_list, lookup_dictionary):
     match_start = datetime.now()
     precise_file = 'searchphrases_fine_matching.csv'
     raw_match_file = 'searchphrases_raw_matching.csv'
     header = [["SKU", "Match Type", "Match Count", "Search Volume", "Search Phrase", "Match Array", "Product Description", "Brand & Category"]]
     write_to_csv(precise_file, header)
     write_to_csv(raw_match_file, header)
     counter = 0
     for searchphrase in lookup_list:
          if counter >= 100:
               counter = 0
               match_stop = datetime.now()
               match_result = match_stop - match_start
               print(match_result/100)
               match_start = datetime.now()
          for searchword, output in searchphrase[0].items():
               match_dbc = { "description":[0], "brand":[0], "category":[0] }
               for description, brand_category_sku in lookup_dictionary.items():
                    split_name = []
                    split_name = str.split(description)
                    for partial_description in split_name:
                         description_match_ratio = difflib.SequenceMatcher(None, searchword, partial_description).real_quick_ratio()
                         if description_match_ratio > 0.85:
                              # Found SKU
                              for key, value in searchphrase[0].items():
                                   split_category = []
                                   split_category = str.split(brand_category_sku[1])
                                   for partial_category in split_category:
                                        category_match_ratio = difflib.SequenceMatcher(None, key, partial_category).real_quick_ratio()
                                        if category_match_ratio > 0.75:
                                             match_dbc["category"][0] = 1
                                             match_dbc["category"].append(key)
                                   split_brand = []
                                   split_brand = str.split(brand_category_sku[0])
                                   for partial_brand in split_brand:
                                        brand_match_ratio = difflib.SequenceMatcher(None, key, partial_brand).real_quick_ratio()
                                        if brand_match_ratio > 0.75:
                                             if not key in match_dbc["category"][1:]:
                                                  match_dbc["brand"][0] = 1
                                                  match_dbc["brand"].append(key)
                                   for partial_description in split_name:
                                        description_match_ratio = difflib.SequenceMatcher(None, key, partial_description).real_quick_ratio()
                                        if description_match_ratio > 0.85:
                                             if not key in match_dbc["category"][1:] and not key in match_dbc["brand"][1:]:
                                                  match_dbc["description"][0] = 1
                                                  match_dbc["description"].append(key)
                              
                              if match_dbc["description"][0] == 1 and match_dbc["category"][0] == 1 and match_dbc["brand"][0] == 1:
                                   match_type = "brand, category & description"
                              if match_dbc["description"][0] == 1 and match_dbc["category"][0] == 0 and match_dbc["brand"][0] == 1:
                                   match_type = "brand & description"
                              if match_dbc["description"][0] == 1 and match_dbc["category"][0] == 1 and match_dbc["brand"][0] == 0:
                                   match_type = "category & description"
                              if match_dbc["description"][0] == 1 and match_dbc["category"][0] == 0 and match_dbc["brand"][0] == 0:
                                   match_type = "only description"
                              if ((len(match_dbc["description"]) - 1) + (len(match_dbc["brand"]) - 1) + (len(match_dbc["category"]) - 1) ) >= len(searchphrase[0]):
                                   match_count = "complete match"
                              else:
                                   match_count = "incomplete  match"
                              searched_words = []
                              for word, empty in searchphrase[0].items():
                                   searched_words.append(word)
                              final_phrase = ' '.join(searched_words)
                              output = [[brand_category_sku[2], match_type, match_count, searchphrase[1], final_phrase, match_dbc, description, brand_category_sku[:2]]]
                              if match_type == "brand, category & description" or match_type == "brand & description":
                                   write_to_csv(precise_file, output)
                              else:
                                   write_to_csv(raw_match_file, output)
                              counter = counter + 1
                         else:
                              pass
                    ### No Product Match ###
                    # Check Category & Brand!
                    if match_dbc == { "description":[0], "brand":[0], "category":[0] }:
                         split_category = []
                         split_category = str.split(brand_category_sku[1])
                         for partial_category in split_category:
                              category_match_ratio = difflib.SequenceMatcher(None, key, partial_category).real_quick_ratio()
                              if category_match_ratio > 0.75:
                                   match_dbc["category"][0] = 1
                                   match_dbc["category"].append(key)
                         split_brand = []
                         split_brand = str.split(brand_category_sku[0])
                         for partial_brand in split_brand:
                              brand_match_ratio = difflib.SequenceMatcher(None, key, partial_brand).real_quick_ratio()
                              if brand_match_ratio > 0.75:
                                   if not key in match_dbc["category"][1:]:
                                        match_dbc["brand"][0] = 1
                                        match_dbc["brand"].append(key)
                         if match_dbc["description"][0] == 1 and match_dbc["category"][0] == 1 and match_dbc["brand"][0] == 1:
                              match_type = "brand, category & description"
                         if match_dbc["description"][0] == 1 and match_dbc["category"][0] == 0 and match_dbc["brand"][0] == 1:
                              match_type = "brand & description"
                         if match_dbc["description"][0] == 1 and match_dbc["category"][0] == 1 and match_dbc["brand"][0] == 0:
                              match_type = "category & description"
                         if match_dbc["description"][0] == 1 and match_dbc["category"][0] == 0 and match_dbc["brand"][0] == 0:
                              match_type = "only description"
                         if ((len(match_dbc["description"]) - 1) + (len(match_dbc["brand"]) - 1) + (len(match_dbc["category"]) - 1) ) >= len(searchphrase[0]):
                              match_count = "complete match"
                         else:
                              match_count = "incomplete  match"
                         searched_words = []
                         for word, empty in searchphrase[0].items():
                              searched_words.append(word)
                         final_phrase = ' '.join(searched_words)
                         output = [[brand_category_sku[2], match_type, match_count, searchphrase[1], final_phrase, match_dbc, description, brand_category_sku[:2]]]
                         if match_type == "brand, category & description" or match_type == "brand & description":
                              write_to_csv(precise_file, output)
                         else:
                              write_to_csv(raw_match_file, output)
                         counter = counter + 1
                    else:
                         pass
               else:
                    pass


def find_residuals(search_input, product_output, category_output, brand_output, residuals_csv):
     pass
     # map each output into dictionary with search phrase as key
     # loop through search phrases
          # find key in search phrases of matched products
               # break
          # find key in search phrase of matched categories
               # break
          # find key in search phrase of matched brands
               # break
          # output residuals


start = datetime.now()
lookup_dict = create_dictionary_from_csv(lookup_csv)
searchword_list = searchword_searchphrase_dict(to_match_csv)
vlookup_similar(searchword_list, lookup_dict)
stop = datetime.now()
result = stop - start
print(result)

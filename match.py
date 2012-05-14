# Fancy Matcher 2.4 - Sebastian Oehlschläger, Torsten Kunz

import csv
import sys
import difflib
from datetime import datetime
 
### write to csv
 
def write_to_csv(target_file, output):
     with open(target_file, 'a', newline='', encoding='latin-1') as f:
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
          if line[1] in lookup_dict and line[2] in lookup_dict[line[1]][0]:
               lookup_dict[line[1]].append(line[0])
          else :
               key_value = {line[1]:[line[2],line[3]+' '+line[4],line[0]]}
               lookup_dict.update(key_value)
     return lookup_dict

def create_searchword_list(csvfile):
     reader = csv.reader(open(csvfile, encoding='latin-1'), delimiter=';')
     searchword_list = []
     for line in reader:
          split_phrase = []
          split_phrase = str.split(line[0])
          searchword_list.append([split_phrase, line[1]])
#          print(searchword_list)
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
     files = {'brand, category & description': {'complete match':'complete_brand_cat_desc.csv','incomplete match':'incomplete_brand_cat_desc.csv'},
              'brand & description': {'complete match':'complete_brand_desc.csv','incomplete match':'incomplete_brand_desc.csv'},
              'category & description': {'complete match':'complete_cat_desc.csv','incomplete match':'incomplete_cat_desc.csv'},
              'only description': {'complete match': 'complete_desc.csv', 'incomplete match':'incomplete_desc.csv'}}
     
     header = [["SKU", "Match Type", "Match Count", "Search Volume", "Search Phrase", "Match Array", "Product Description", "Brand & Category"]]

     for key, value in files.items():
          for key, file in value.items():
               write_to_csv(file, header)

     counter = 0

     for searchphrase in lookup_list:
          counter = counter + 1
          if counter >= 100:
               counter = 0
               match_stop = datetime.now()
               match_result = match_stop - match_start
               print(match_result/100)
               match_start = datetime.now()

          for searchword in searchphrase[0]:     

               for description, brand_category_sku in lookup_dictionary.items():
                    match_dbc = { "description":[0], "brand":[0], "category":[0] }
                    split_name = []
                    split_name = str.split(description)

                    for partial_name in split_name:
                         name_match_ratio = difflib.SequenceMatcher(None, searchword, partial_name).ratio()
                         if name_match_ratio > 0.85:
                              # Found SKU

                              for key in searchphrase[0]:

                                   split_category = []
                                   split_category = str.split(brand_category_sku[1])
                                   for partial_category in split_category:
                                        category_match_ratio = difflib.SequenceMatcher(None, key, partial_category).ratio()
                                        if category_match_ratio > 0.75:
                                             if not key in match_dbc["category"][1:]:
                                                  match_dbc["category"][0] = 1
                                                  match_dbc["category"].append(key)


                                   split_brand = []
                                   split_brand = str.split(brand_category_sku[0])

                                   for partial_brand in split_brand:
                                        brand_match_ratio = difflib.SequenceMatcher(None, key, partial_brand).ratio()
                                        if brand_match_ratio > 0.75:
                                             if not key in match_dbc["category"][1:] and not key in match_dbc["brand"][1:]:
                                                  match_dbc["brand"][0] = 1
                                                  match_dbc["brand"].append(key)

                                   split_description = []
                                   split_description = str.split(description)
                                   # desc_m_r_list = []
                                   for partial_description in split_description:
                                        description_match_ratio = difflib.SequenceMatcher(None, key, partial_description).ratio()
                                   #     desc_m_r_list.append(description_match_ratio)
                                        if description_match_ratio > 0.85:
                                             if not key in match_dbc["category"][1:] and not key in match_dbc["brand"][1:] and not key in match_dbc["description"][1:]:
                                                  match_dbc["description"][0] = 1
                                                  match_dbc["description"].append(key+'-'+partial_description+'-'+str(description_match_ratio))
                                        else:
                                             pass

                              match_type = "empty"
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
                                   match_count = "incomplete match"
                              searched_words = []

                              for word in searchphrase[0]:
                                   searched_words.append(word)
                              final_phrase = ' '.join(searched_words)
                              output = [[brand_category_sku[2], match_type, match_count, searchphrase[1], final_phrase, match_dbc, description, brand_category_sku[:2]]]
                              if not match_type == "empty":
                                   write_to_csv(files[match_type][match_count], output)
                              counter = counter + 1
                         else:
                              pass

##                    ### No Product Match    ###
##                    # Check Category & Brand!
##                    if match_dbc == { "description":[0], "brand":[0], "category":[0] }:
##                         for key, value in searchphrase[0].items():
##                              split_category = []
##                              split_category = str.split(brand_category_sku[1])
##                              for partial_category in split_category:
##                                   category_match_ratio = difflib.SequenceMatcher(None, key, partial_category).ratio()
##                                   if category_match_ratio > 0.75:
##                                        match_dbc["category"][0] = 1
##                                        match_dbc["category"].append(key)
##                              split_brand = []
##                              split_brand = str.split(brand_category_sku[0])
##                              for partial_brand in split_brand:
##                                   brand_match_ratio = difflib.SequenceMatcher(None, key, partial_brand).ratio()
##                                   if brand_match_ratio > 0.75:
##                                        if not key in match_dbc["category"][1:]:
##                                             match_dbc["brand"][0] = 1
##                                             match_dbc["brand"].append(key)
##                         if not match_dbc == { "description":[0], "brand":[0], "category":[0] }:
##                              if match_dbc["category"][0] == 1 and match_dbc["brand"][0] == 1:
##                                   match_type = "brand & category"
##                              if match_dbc["category"][0] == 0 and match_dbc["brand"][0] == 1:
##                                   match_type = "brand"
##                              if match_dbc["category"][0] == 1 and match_dbc["brand"][0] == 0:
##                                   match_type = "category"
##                              if ((len(match_dbc["brand"]) - 1) + (len(match_dbc["category"]) - 1)) >= len(searchphrase[0]):
##                                   match_count = "complete match"
##                              else:
##                                   match_count = "incomplete  match"
##                              searched_words = []
##                              for word, empty in searchphrase[0].items():
##                                   searched_words.append(word)
##                              final_phrase = ' '.join(searched_words)
##                              output = [[brand_category_sku[2], match_type, match_count, searchphrase[1], final_phrase, match_dbc, description, brand_category_sku[:2]]]
##                              if match_type == "brand & category":
##                                   write_to_csv(brand_category_match_file, output)
##                              else:
##                                   write_to_csv(raw_category_match_file, output)
##                                   
##                         else:
##                              pass
##               else:
##                    pass
##
##def create_output_dictionaries_from_csv(csvfile):
##     reader = csv.reader(open(csvfile, encoding='latin-1'), delimiter=';')
##     output_dict = {}
##     for line in reader:
##          key_value = {line[4]:line[1]}
##          output_dict.update(key_value)
##     return output_dict
##
##def find_residuals(search_input):
##     residuen_csv = 'residuen_list.csv'
##     searchphrases_fine_matching_dict = create_output_dictionaries_from_csv('searchphrases_fine_matching.csv')
##     searchphrases_raw_category_matching_dict = create_output_dictionaries_from_csv('searchphrases_raw_category_matching.csv')
##     searchphrases_brand_category_matching_dict = create_output_dictionaries_from_csv('searchphrases_brand_category_matching.csv')
##     searchphrases_raw_matching_dict = create_output_dictionaries_from_csv('searchphrases_raw_matching.csv')
##
##     for searchphrase in search_input:
##          words = []
##          for key in searchphrase[0]:
##               words.append(key)
##          phrase = ' '.join(words)
##          try:
##               output = searchphrases_fine_matching_dict[phrase]
##          except:
##               try:
##                    output = searchphrases_raw_matching_dict[phrase]
##               except:
##                    try:
##                         output = searchphrases_brand_category_matching_dict[phrase]
##                    except:
##                         try:
##                              output = searchphrases_raw_category_matching_dict[phrase]
##                         except:
##                              output = "Residuals"
##          matched_phrase = [[phrase, output]]
##          write_to_csv(residuen_csv, matched_phrase)

lookup_dict = create_dictionary_from_csv(lookup_csv)
searchword_list = create_searchword_list(to_match_csv)
start = datetime.now()
print(start)
vlookup_similar(searchword_list, lookup_dict)
#find_residuals(searchword_list)

stop = datetime.now()
result = stop - start
print(result)



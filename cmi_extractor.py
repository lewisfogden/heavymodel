# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 16:15:11 2020

@author: user
"""

# CMI Table Extractor

import pandas as pd
import random
import timeit
random.seed(0)

xlsx_file = r"D:\dev\heavymodel\models\tables\CMI WP120 Final IP06 claim inception rates v01 2019-03-27.xlsx"

sheets_to_read = ["DP1", "DP4", "DP13", "DP26", "DP52"]
sheet_list = []

for sheet in sheets_to_read:
    df = pd.read_excel(xlsx_file, sheet_name=sheet, header=5)
    df = df.melt(id_vars=["Age"], var_name="Key", value_name="Rate")
    sheet_list.append(df)

full_table = pd.concat(sheet_list)
full_table.set_index(["Key", "Age"], inplace=True)

# test a few values

test_cases = [ ("IP06 F DP1 OC1", 30, 0.034012),
               ("IP06 M DP26 OC3", 45, 0.002223),
               ("IP06 M DP52 OC4", 49, 0.002072)
               ]

for key, age, result in test_cases:
    print(key, age, float(full_table.loc[key, age]), result)


# comparison to storing in a dictionary
full_dict = full_table.to_dict()["Rate"]

# build a random test set of 1000 keys

sample = random.sample(full_dict.keys(), 1000)

# time getting keys

def dict_sample_func():
    total = 0
    for key,age in sample:
        total += full_dict[key, age]
    return total

def df_sample_func():
    total = 0
    for key, age in sample:
        total += float(full_table.loc[key, age])
    return total

# is a split key faster than a single key?
split_sample = [(*(k[0].split(" ")),k[1]) for k in sample]

split_dict = {(*(k[0].split(" ")),k[1]): v for k, v in full_dict.items()}

def split_dict_sample_func():
    total = 0
    for key in split_sample:
        total += split_dict[key]
    return total

# is it faster to concatenate keys by hand?

def concat_sample_func():
    total = 0
    for code, sex, dp, occ, age in split_sample:
        total += full_dict[" ".join([code, sex, dp, occ]), age]
    return total

dict_speed = timeit.timeit(dict_sample_func, number=10)
df_speed = timeit.timeit(df_sample_func, number=10)
split_dict_speed = timeit.timeit(split_dict_sample_func, number=10)

# dictionary of dictionary approach
dict_of_full_dict = {}
for k, v in full_dict.items():
    if k[0] not in dict_of_full_dict:
        dict_of_full_dict[k[0]] = {}
    dict_of_full_dict[k[0]][k[1]] = v

def dict_of_dict_func():
    total = 0
    for key, age in sample:
        total += dict_of_full_dict[key][age]
    return total

# Conclusion
# Dictionary is much faster than dataframe (10x)
# Using less keys is faster
# nesting dictionaries is faster than having tuple keys
# recommended is merging all keys which are invariant in a run into a string
# e.g. self.female_table = "IP06 F DP1 OC1"





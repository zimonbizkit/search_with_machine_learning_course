import os
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv
import re

# Useful if you want to perform stemming.
import nltk
stemmer = nltk.stem.PorterStemmer()

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/fasttext/labeled_queries.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1000,  help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

pd.set_option('display.max_rows', None)


if args.min_queries:
    min_queries = int(args.min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(list(zip(categories, parents)), columns =['category', 'parent'])

# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
queries_df = pd.read_csv(queries_file_name)[['category', 'query']]
queries_df = queries_df[queries_df['category'].isin(categories)]

# IMPLEMENT ME: Convert queries to lowercase, and optionally implement other normalization, like stemming.

queries_df['query'] = queries_df['query'].apply(lambda x: re.sub('[^a-zA-Z\d\s:]', ' ',str(x) ) ).apply(lambda x: re.sub('\ +', ' ', str(x)))
queries_df['query'] = queries_df['query'].apply(lambda x: stemmer.stem(x))

cat_counts_df = queries_df.groupby('category').count()
cat_counts_df.rename(columns={'query':'query_count'},inplace=True)


#print(cat_counts_df[(cat_counts_df['category'])=='abcat0701001'].head(1))

# IMPLEMENT ME: Roll up categories to ancestors to satisfy the minimum number of queries per category.




#joined_df = queries_df.set_index('category').join(cat_counts_df_below_100.set_index('category'))
#merged_df = pd.merge(queries_df,cat_counts_df_below_100,how='outer')




# Roll up categories to ancestors to satisfy the minimum number of queries per category.
#print(queries_df.head(10))
#print(parents_df.head(10))
#print(cat_counts_df.head(10))
print("rolling up categories")
while True:
    cat_count =  queries_df.groupby(['category']).size().reset_index(name="total_queries")
    df_below_minimum = cat_count[cat_count["total_queries"] < min_queries]["category"].unique()
    if df_below_minimum.any():
        parent_cat = queries_df.merge(parents_df, on="category", how="left")
        parent_cat["parent"].loc[pd.isnull] = root_category_id
        parent_df = parent_cat.merge(cat_count, on="category",  how="left")
        parent_df.loc[parent_df["total_queries"] < min_queries, "category"] = parent_df["parent"]
        queries_df = parent_df.drop(["parent", "total_queries"], axis=1)
    else:
        break


    

    
print('Categories rolled up, number of rolledup categories is')

print(queries_df['category'].unique().size)
# Create labels in fastText format.
queries_df['label'] = '__label__' + queries_df['category']

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
queries_df = queries_df[queries_df['category'].isin(categories)]
queries_df['output'] = queries_df['label'] + ' ' + queries_df['query']
queries_df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)

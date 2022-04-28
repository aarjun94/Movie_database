from bs4 import BeautifulSoup
from openpyxl import load_workbook
from py import builtin
import json
from Main import *
import pprint



first_op = ['TV', 'Movie']
genre_op = ['Comedy', 'Drama', 'Romance', 'Crime', 'Animation', 'Family', 'Mystery', 'Fantasy', 'Thriller', 'Action', 'Adventure', 'History', 'War', 'Western', 'Science Fiction', 'Horror', 'TV Movie'\
    'Music', 'Reality', 'Sci-Fi & Fantasy', 'Action & Adventure']
language_op = ['fr', 'es', 'hi', 'ja', 'ko', 'en']
year_op = [str(x) for x in range(1990, 2023)]


def create_tree():
    
    for f in first_op:
        tree[f] = {}
        for l in language_op:
            tree[f][l] = {}
            for g in genre_op:
                g_val = access_genre_sql_database(g,f)
                tree[f][l][g] = {}
                for y in year_op:
                    temp = db_to_dict(f, l, g_val, y)
                    temp = [item for t in temp for item in t]
                    tree[f][l][g][y] = temp
    return tree
data = create_tree()
with open('tree.json', 'w') as f:
    json.dump(data, f)
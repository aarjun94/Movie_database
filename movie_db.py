import pandas as pd
import requests
import csv

api_key = "9c601f958ba38d1f21e27b94cf35dd38"
link = "https://api.themoviedb.org/3/movie/top_rated?"
response = requests.get(f"{link}api_key={api_key}&language=en-US&page=1")

# link = "https://api.themoviedb.org/3/movie/24001?"
# response = requests.get(f"{link}api_key={api_key}&language=en-US")

response.json()


data = pd.DataFrame(response.json()["results"])[['genre_ids','id','title','overview','popularity','release_date','vote_average','vote_count']]

for i in range(2, 493):
    response = requests.get("https://api.themoviedb.org/3/movie/top_rated?api_key=9c601f958ba38d1f21e27b94cf35dd38&language=en-US&page={}".format(i))
    temp_df = pd.DataFrame(response.json()["results"])[['genre_ids','id','title','overview','popularity','release_date','vote_average','vote_count']]
    data = data.append(temp_df, ignore_index=False)


data_id = list(data['id'])
data_id

genre = []
def genre_info(item):
    api_key = "9c601f958ba38d1f21e27b94cf35dd38"
    link = f"https://api.themoviedb.org/3/movie/{item}?"
    response = requests.get(f"{link}api_key={api_key}&language=en-US")
    y = response.json()['genres']
    genre.append(y)

lan = []
def language_info(item):
    api_key = "9c601f958ba38d1f21e27b94cf35dd38"
    link = f"https://api.themoviedb.org/3/movie/{item}?"
    response = requests.get(f"{link}api_key={api_key}&language=en-US")
  
    y = response.json()['original_language']
            
    lan.append(y)

imdb_id = []
def imdb_info(item):
    api_key = "9c601f958ba38d1f21e27b94cf35dd38"
    link = f"https://api.themoviedb.org/3/movie/{item}?"
    response = requests.get(f"{link}api_key={api_key}&language=en-US")
  
    y = response.json()['imdb_id']

    imdb_id.append(y)


import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(genre_info, data_id)

import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(language_info, data_id)

import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(imdb_info, data_id)

data['language'] = lan

data['imdb_id'] = imdb_id

import collections
freq = collections.Counter(lan)

x_sorted = dict(sorted(dict(freq).items(), key=lambda item:item[1]))

genre_id = list(data['genre_ids'])

genre_info = {}
unique_ids = {}
for id_list in genre:
  for id_val in id_list:
    unique_ids[id_val['id']] = id_val['name']


data.to_csv('movie.csv')


with open('genre.csv', 'w') as f:
    for key in unique_ids.keys():
        f.write("%s, %s\n" % (key, unique_ids[key]))


import pandas as pd
import requests
import csv

api_key = "9c601f958ba38d1f21e27b94cf35dd38"
link = "https://api.themoviedb.org/3/tv/top_rated?"
response = requests.get(f"{link}api_key={api_key}&language=en-US&page=1")

data = pd.DataFrame(response.json()["results"])[['genre_ids','id','name','overview','popularity','first_air_date','vote_average','vote_count']]

for i in range(2, 119):
    response = requests.get("https://api.themoviedb.org/3/tv/top_rated?api_key=9c601f958ba38d1f21e27b94cf35dd38&language=en-US&page={}".format(i))
    temp_df = pd.DataFrame(response.json()["results"])[['genre_ids','id','name','overview','popularity','first_air_date','vote_average','vote_count']]
    data = data.append(temp_df, ignore_index=False)

data_id = list(data['id'])

genre = []
def genre_info(item):
    api_key = "9c601f958ba38d1f21e27b94cf35dd38"
    link = f"https://api.themoviedb.org/3/tv/{item}?"
    response = requests.get(f"{link}api_key={api_key}&language=en-US")
  
    y = response.json()['genres']
            
    genre.append(y)

lan = []
def language_info(item):
    api_key = "9c601f958ba38d1f21e27b94cf35dd38"
    link = f"https://api.themoviedb.org/3/tv/{item}?"
    response = requests.get(f"{link}api_key={api_key}&language=en-US")
  
    y = response.json()['original_language']
            
    lan.append(y)

import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(genre_info, data_id)

import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(language_info, data_id)

data['language'] = lan

genre_id = list(data['genre_ids'])

genre_info = {}
unique_ids = {}
for id_list in genre:
  for id_val in id_list:
    unique_ids[id_val['id']] = id_val['name']

data.to_csv('tv.csv')

with open('genre_tv.csv', 'w') as f:
    for key in unique_ids.keys():
        f.write("%s, %s\n" % (key, unique_ids[key]))
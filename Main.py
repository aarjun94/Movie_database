from bs4 import BeautifulSoup
from openpyxl import load_workbook
import plotly.graph_objs as go
import plotly.figure_factory as ff
from py import builtin
import requests
import json
import webbrowser
import csv
import sqlite3
import time
import pprint

CACHE_FILENAME = "movie_cache.json"
CACHE_DICT = {}
DB_NAME = "movie.sqlite"



def create_database():
    ''' Creates a SQL database with 4 tables: "Movie", "TV" and two "Genre" tables each for Movie and TV. 

    PARAMETERS
    ----------
    none

    RETURNS
    -------
    none
    '''

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    drop_movie_sql = "DROP TABLE IF EXISTS 'Movie'"
    drop_tv_sql = "DROP TABLE IF EXISTS 'TV'"
    drop_genre_sql = "DROP TABLE IF EXISTS 'Genre'"
    drop_genre_tv_sql = "DROP TABLE IF EXISTS 'Genretv'"


    create_movie_sql = '''
        CREATE TABLE IF NOT EXISTS "Movie" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "IMDB" TEXT NOT NULL,
            "Title" TEXT NOT NULL,
            "Overview" TEXT NOT NULL,
            "Popularity" FLOAT NOT NULL,
            "Release_date" DATETIME NOT NULL,
            "Vote Average" FLOAT,
            "Vote Count" INTEGER NOT NULL,
            "Genre_ID" TEXT NOT NULL,
            "language" TEXT NOT NULL
        )
    '''

    create_tv_sql = '''
        CREATE TABLE IF NOT EXISTS "TV" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Title" TEXT NOT NULL,
            "Overview" TEXT NOT NULL,
            "Popularity" FLOAT NOT NULL,
            "Release_date" DATETIME NOT NULL,
            "Vote Average" FLOAT,
            "Vote Count" INTEGER NOT NULL,
            "Genre_ID" TEXT NOT NULL,
            "language" TEXT NOT NULL
        )
    '''

    create_genre_sql = '''
        CREATE TABLE IF NOT EXISTS "Genre" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Genre_ID" INTEGER NOT NULL,
            "Genre_Name" TEXT NOT NULL
        )
    '''

    create_genre_tv_sql = '''
        CREATE TABLE IF NOT EXISTS "Genretv" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Genre_ID" INTEGER NOT NULL,
            "Genre_Name" TEXT NOT NULL
        )
    '''

    cur.execute(drop_movie_sql)
    cur.execute(drop_tv_sql)
    cur.execute(drop_genre_sql)
    cur.execute(drop_genre_tv_sql)
    cur.execute(create_movie_sql)
    cur.execute(create_tv_sql)
    cur.execute(create_genre_sql)
    cur.execute(create_genre_tv_sql)

    conn.commit()
    conn.close()

def populate_database():
    ''' Populates 2 tables in SQL database with data from a variety of sources.
    
    PARAMETERS
    ----------

    RETURNS
    -------
    '''

    data_header = []
    data_rows = []

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    with open("Data/movie.csv", 'r') as csvfile:
        data = []
        csv_header = csv.reader(csvfile)
        for h in csv_header:
            data.append(h)
        data_header.extend(data[0])
        data_rows.extend(data[1:])

    insert_movie_sql = '''
        INSERT INTO Movie
        VALUES (NULL, ?, ? , ?, ?, ?, ?, ?, ?, ?)
    '''

    for dr in data_rows:
        cur.execute(insert_movie_sql, [
            dr[-1],
            dr[3],
            dr[4],
            dr[5],
            dr[6],
            dr[7],
            dr[8],
            dr[1],
            dr[9],
        ])

    
    data_header_tv = []
    data_rows_tv = []

    with open("Data/tv.csv", 'r') as csvfile:
        data_tv = []
        csv_header = csv.reader(csvfile)
        for h in csv_header:
            data_tv.append(h)
        data_header_tv.extend(data[0])
        data_rows_tv.extend(data[1:])

    insert_tv_sql = '''
        INSERT INTO TV
        VALUES (NULL, ?, ? , ?, ?, ?, ?, ?, ?)
    '''

    for dr in data_rows:
        cur.execute(insert_tv_sql, [
            dr[3],
            dr[4],
            dr[5],
            dr[6],
            dr[7],
            dr[8],
            dr[1],
            dr[9],
        ])

    data_rows_genre = []

    with open("Data/genre.csv", 'r') as csvfile:
        data_genre = []
        csv_header = csv.reader(csvfile)
        for h in csv_header:
            data_genre.append(h)
        data_rows_genre.extend(data_genre[:])
    
    insert_genre_sql = '''
        INSERT INTO Genre
        VALUES (NULL, ?, ?)
    '''

    for dr in data_rows_genre:
        cur.execute(insert_genre_sql, [
            dr[0],
            dr[1]
        ])
    
    data_rows_genre_tv = []

    with open("Data/genre_tv.csv", 'r') as csvfile:
        data_genre = []
        csv_header = csv.reader(csvfile)
        for h in csv_header:
            data_genre.append(h)
        data_rows_genre_tv.extend(data_genre[:])
    
    insert_genre_tv_sql = '''
        INSERT INTO Genretv
        VALUES (NULL, ?, ?)
    '''

    for dr in data_rows_genre_tv:
        cur.execute(insert_genre_tv_sql, [
            dr[0],
            dr[1]
        ])

    conn.commit()
    conn.close()

def movie_info(imdb_id):
    url = "http://www.omdbapi.com/?"
    API_key = "23fd4044"
    movie_infomation= requests.get(f"{url}apikey={API_key}&i={imdb_id}").json()
    info = {'director':[movie_infomation['Director']], 'actor_list':movie_infomation['Actors'].split(', '), 'poster': movie_infomation['Poster'], 'imbd_rating': movie_infomation['imdbRating'] }
    return info

def access_movie_sql_database(title):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    query = f'''
        SELECT *
        FROM Movie
        WHERE Title = "{title}"
    '''
    result = cur.execute(query).fetchall()
    conn.close()
    return result


def access_genre_sql_database(genre, f):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    query = f'''
        SELECT Genre_ID
        FROM {f}
        WHERE  Genre_Name = " {genre}"
    '''

    result = cur.execute(query).fetchall()
    conn.close()
    return result[0][0]

def db_to_dict(f, l, g, y):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    query = f'''
        SELECT Title
        FROM {f}
        WHERE language = "{l}"
        AND Genre_ID LIKE "%{g}%"
        AND Release_date LIKE "{y}%"
    '''
    result = cur.execute(query).fetchall()
    conn.close()

    return result

first_op = ['TV Show', 'Movie']
genre_op = ['Thriller', 'Horror']
language_op = ['fr', 'es']
year_op = ['2020', '2019']
tree = {}

def create_tree():
    for f in first_op:
        tree[f] = {}

        for l in language_op:
            tree[f][l] = {}
            for g in genre_op:
                x = 'Genre' if f == 'Movie' else 'Genretv'
                g_val = access_genre_sql_database(g, x) 
                tree[f][l][g] = {}
                for y in year_op:
                    temp = db_to_dict(f, l, g_val, y)
                    temp = [item for t in temp for item in t]
                    tree[f][l][g][y] = temp
    return tree


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    dict:
        The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def make_request_with_cache(cache_key, cache_value):

    '''Check the cache for a saved result for this cache_key:cache_value
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    cache_key: string
        Various strings to be used as keys in CACHE_DICT
    cache_value: string
        Information to be saved as the value in CACHE_DICT
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    if cache_key in CACHE_DICT.keys():
        # print("Using cache")
        return CACHE_DICT[cache_key]
    else:
        # print("Fetching")
        CACHE_DICT[cache_key] = cache_value
        save_cache(CACHE_DICT)
        return CACHE_DICT[cache_key]

def actor_profile(keyword):
    ''' Scrapes USDA ERS county-level datasets webpage and creates a dictionary for each dataset and its corresponding URL.

    PARAMETERS
    ----------
    none

    RETURNS
    -------
    dict:
        Dictionary of 4 county-level data sets available from the USDA ERS and their respective URLs.
    '''

    url = f"https://en.wikipedia.org/wiki/{keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    make_request_with_cache(url, soup.prettify())
    
    section = soup.find("table", {"class":"infobox biography vcard"})
    return section

if __name__ == "__main__":
    CACHE_DICT = open_cache()
    create_database()
    populate_database()

    # conn = sqlite3.connect(DB_NAME)
    # cur = conn.cursor()
    # query = f'''
    #     SELECT Title
    #     FROM Movie
    #     WHERE Release_date LIKE '2011%'
    # '''
    # result = cur.execute(query).fetchall()
    # conn.close()
    # print(result)


    # pprint.pprint(foo())

    # x = actor_profile('The_Shawshank_Redemption')
    # print(x)

    url = "https://www.imdb.com/title/tt0111161/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    make_request_with_cache(url, soup.prettify())
    
    section = soup.find("li", {"class":"ipc-metadata-list__item sc-3c7ce701-2 eYXppQ"})
    # indiv = section.find("ul")
    print(section.text.strip())


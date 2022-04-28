from bs4 import BeautifulSoup
from django.http import response
from openpyxl import load_workbook
from py import builtin
import requests
import json
import csv
import sqlite3
import re
from flask import Flask,render_template,request
import pandas as pd
import requests
from bs4 import BeautifulSoup

CACHE_FILENAME = "movie_cache.json"
CACHE_DICT = {}
DB_NAME = "movie.sqlite"



tree = {}
api_key = "9c601f958ba38d1f21e27b94cf35dd38"
data = pd.read_csv("/Users/arjunanandapadmanabhan/Desktop/Projects/507_Final_Project/Data/tv.csv")

tv_dict = {}
tv_id = data['id']
tv_title = data['name']
for name, item in zip(tv_title, tv_id):
    tv_dict[name] = item

app = Flask(__name__)
 
@app.route('/')
def index():
    
    return render_template('index.html')

main_dict = {}

@app.route('/first_option', methods = ['GET'])
def first_opt():
    if request.method == 'GET':
        return render_template('First_option.html')    
        # if request.method == 'POST':
        # temp = request.form.get("xxx")
        # print(temp)
        

@app.route('/language', methods = ['POST', 'GET'])
def lang():
    global main_dict
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        temp = request.form.get("firstop")
        main_dict['firstop'] = temp
        return render_template('language.html')

@app.route('/genre', methods = ['POST', 'GET'])
def genre():
    global main_dict
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        temp = request.form.get("language")
        main_dict['language'] = temp
        if main_dict['firstop'] == "Movie":
            return render_template('genremovie.html')
        else:
            return render_template('genretv.html')

@app.route('/year', methods = ['POST', 'GET'])
def year():
    global main_dict
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        temp = request.form.get("genre")
        main_dict['genre'] = temp
        return render_template('year.html')

@app.route('/title', methods = ['POST', 'GET'])
def final():
    global main_dict, tree
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        temp = request.form.get("year")
        main_dict['year'] = temp
        d = {}
        t = []
        if temp == "a":
            for i in range(1990, 2001):
                temp = tree[main_dict['firstop']][main_dict['language']][main_dict['genre']][str(i)]
                for x in temp: 
                    t.append(x)
        elif temp == "b":
            for i in range(2001, 2006):
                temp = tree[main_dict['firstop']][main_dict['language']][main_dict['genre']][str(i)]
                for x in temp: 
                    t.append(x)
        elif temp == "c":
            for i in range(2006, 2011):
                temp = tree[main_dict['firstop']][main_dict['language']][main_dict['genre']][str(i)]
                for x in temp: 
                    t.append(x)
        elif temp == "d":
            for i in range(2011, 2016):
                temp = tree[main_dict['firstop']][main_dict['language']][main_dict['genre']][str(i)]
                for x in temp: 
                    t.append(x)
        elif temp == "e":
            for i in range(2016, 2021):
                temp = tree[main_dict['firstop']][main_dict['language']][main_dict['genre']][str(i)]
                for x in temp: 
                    t.append(x)
        elif temp == "f":
            for i in range(2021, 2023):
                temp = tree[main_dict['firstop']][main_dict['language']][main_dict['genre']][str(i)]
                for x in temp: 
                    t.append(x)
        if t:
            return render_template('title.html', len = len(t), t = t)
        else:
            return render_template('error.html')

@app.route('/title2', methods = ['POST', 'GET'])
def final2():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    
    if request.method == 'POST':
        temp = request.form.get("title")
        d= {}
        if main_dict['firstop'] == 'Movie':
                res = access_movie_sql_database(temp)[0]
                try: 
                    poster = requests.get(f"https://api.themoviedb.org/3/movie/{res[-1]}?api_key={api_key}").json()['poster_path']
                    poster_url = "https://image.tmdb.org/t/p/w500" + poster
                except:
                    poster= "https://imdb-api.com/posters/original/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg"
                imdb_rating = movie_info(res[-1])['imbd_rating']
                actors = movie_info(res[-1])['actor_list']
                actor_picture = [actor_profile(item) for item in actors]
                d[temp] = {'Desc': res[0], 'Pop': res[1], 'Year': res[2][:4], 'imdb': res[3], 'poster':poster_url, 'rating':imdb_rating, 'genre': main_dict['genre'], 'actor':actors, 'actor_picture':actor_picture}
        else:
                res = access_movie_sql_database(temp, 'TV')[0]
                item = tv_dict[temp]
                response = requests.get(f"http://api.themoviedb.org/3/tv/{item}?api_key={api_key}&append_to_response=external_ids").json()['external_ids']['imdb_id']
                poster = requests.get(f"https://api.themoviedb.org/3/tv/{item}/season/1/images?api_key={api_key}").json()['posters'][0]["file_path"]
                poster_url = "https://image.tmdb.org/t/p/w500" + poster
                imdb_rating = movie_info(response)['imbd_rating']
                actors = movie_info(response)['actor_list']
                actor_picture = [actor_profile(item) for item in actors]
                d[temp] = {'Desc': res[0], 'Pop': res[1], 'Year': res[2][:4], 'imdb': response, 'poster': poster_url, 'genre':main_dict['genre'], 'rating': imdb_rating, 'actor':actors, 'actor_picture':actor_picture}
        return render_template('title2.html', len = len(actor_picture),t = d)

@app.route('/index', methods = ['POST', 'GET'])
def error():
    if request.method == 'POST':
        return render_template('index.html')

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
        data_header_tv.extend(data_tv[0])
        data_rows_tv.extend(data_tv[1:])

    insert_tv_sql = '''
        INSERT INTO TV
        VALUES (NULL, ?, ? , ?, ?, ?, ?, ?, ?)
    '''

    for dr in data_rows_tv:
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
    ''' The function takes in IMDB ID as input and retrives the movie information including actors, directors and IMDB rating from OMDB API. 
    
    PARAMETERS
    ----------
    imdb_id: String

    RETURNS
    -------
    info: A dictionary with the cast and crew information and IMDB rating. 
    '''
    url = "http://www.omdbapi.com/?"
    API_key = "23fd4044"
    movie_infomation= requests.get(f"{url}apikey={API_key}&i={imdb_id}").json()
    info = {'director':[movie_infomation['Director']], 'actor_list':movie_infomation['Actors'].split(', '), 'poster': movie_infomation['Poster'], 'imbd_rating': movie_infomation['imdbRating'] }
    return info

def access_movie_sql_database(title, option=None):
    ''' The function access the movie database and retrieves information of a particular movie from the database based on "Movie/TV show title".
    
    PARAMETERS
    ----------
    title: String
    option: It can be "TV" or None

    RETURNS
    -------
    result: A dictionary containg overview, popularity score and release date of the movie (retrived from the database)
    '''
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if option:
        query = f'''
            SELECT Overview, Popularity, Release_date 
            FROM TV
            WHERE Title = "{title}"
        '''
    else:
        query = f'''
            SELECT Overview, Popularity, Release_date, IMDB
            FROM MOVIE
            WHERE Title = "{title}"
        '''
    result = cur.execute(query).fetchall()
    conn.close()
    return result


def access_genre_sql_database(genre, f):
    ''' The function access the genre database and retrieves genre_id from the database based on "genre_name".
    
    PARAMETERS
    ----------
    genre: String, genre name
    f: string (Movie/TV)

    RETURNS
    -------
    result: genre id
    '''
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if f=='Movie':
        s = ""
    else:
        s = 'tv'
    query = f'''
        SELECT Genre_ID
        FROM Genre{s}
        WHERE Genre_Name = " {genre}"
    '''

    result = cur.execute(query).fetchall()
    conn.close()

    if result == []:
        return []
    else:
        return result[0][0]


def db_to_dict(f, l, g, y):
    ''' The function access the movie database and retrieves information the database based on multiple parameters and returns a dictionary. 
    
    PARAMETERS
    ----------
    f: String, Movie/TV
    l: string (language)
    g: string(genre)
    y: int(year)

    RETURNS
    -------
    result: a dictonary containing the movie information based on the parameters. 
    '''
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

def acccess_genre_name(genre_id, option=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if option:
        query = f'''
            SELECT Genre_Name
            FROM Genretv
            WHERE Genre_ID = "{genre_id}"
        '''
    result = cur.execute(query).fetchall()
    conn.close()

    return result

first_op = ['TV', 'Movie']
genre_op = ['Comedy', 'Drama', 'Romance', 'Crime', 'Animation', 'Family', 'Mystery', 'Fantasy', 'Thriller', 'Action', 'Adventure', 'History', 'War', 'Western', 'Science Fiction', 'Horror', 'TV Movie'\
    'Music', 'Reality', 'Sci-Fi & Fantasy', 'Action & Adventure', 'Documentary', 'War & Politics', 'Kids', 'Soap', 'Talk', 'News', 'Musical']
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
    ''' The function scrapes the wikipedia webpage for actor picture based on the keyword parameter and returns the picture URL.  
    
    PARAMETERS
    ----------
    keyword: String (actor name)

    RETURNS
    -------
    person_url: a url for the actors picture. 
    '''


    person_url = []
    urlpage =  'https://en.wikipedia.org/wiki/' + keyword
    page = requests.get(urlpage).text
    soup = BeautifulSoup(page, 'html.parser')
    make_request_with_cache(urlpage, soup.prettify())
    
    for raw_img in soup.find_all('img'):
        link = raw_img.get('src')
        if re.search('wikipedia/.*/thumb/', link) and not re.search('.svg', link):
            person_url = [link[2:]]
            break
    return person_url[0]

if __name__ == "__main__":
    CACHE_DICT = open_cache()
    create_database()
    populate_database()
    tree = create_tree()
    app.run(debug=True)






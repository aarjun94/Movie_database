# MOVIE SEARCH ENGINE

# INTRODUCTION
This file is uploaded as a part of the final project requirement for SI 507, Intermediate Programming at University of Michigan, Ann Arbor. The Movie Database API and OMDB API was used to gather information for the movies and TV shows to create a database and visualizations. 

# Required Packages:
1. Flask (pip install FLASK)
2. Pandas (pip install pandas). 
3. Requests (pip install requests)
4. Sqlite3 (pip install sqlite3)
5. re
6. Beautiful Soup (pip install bs4)

# API Keys:
The API key for Movie Database should be saved in a variable "api_key" inside Main.py. The API key can be requested from the site :https://developers.themoviedb.org/3/getting-started. 
The API key for OMDB database should be saved in a variable "API_key" inside movie_info function (Main.py). The API key can be requested from the site: http://www.omdbapi.com/

# Interaction
All files in the githhub repo should be dowloaded and saved inside a single folder. Open the folder in Visual Studio. 
Create a virtual environment before installing the flask. 
Create an environment:
For Mac:
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv

For Windows:
> mkdir myproject
> cd myproject
> py -3 -m venv venv

Activate the environment:
Mac: $ . venv/bin/activate
Windows: > venv\Scripts\activate

For more documentation, please visit: https://flask.palletsprojects.com/en/2.1.x/installation/

After the installation of the flask, the user can run the Main.py program. The user will recieve a link, similar to "http://127.0.0.1:5000/" for the local host server. The user will be guided through a couple of options, for instance, Movie/TV show, Genre, Language and Year. 
Based on the input, a list of top rated Movies or Tv shows will be shown to the user.  The user can select any one of the title for more information on the TV show or Movie. The final display also contains the IMDB rating, a link to the IMDB website, a short description of the selected title along with the main actors name and picture. 




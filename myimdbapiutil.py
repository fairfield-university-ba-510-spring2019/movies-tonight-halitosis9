""""A useful utility for querying IMDB"""
__author__ = "Christopher Huntley"

# imports from Python standard libraries
import pandas as pd
import requests
import urllib.parse
from pandas.io.json import json_normalize

def imdb_import_movie(mid=None,mtitle=None,year=None):
    """Uses the IMDB API to look up movie information

    mid -- the IMDB movie id (optional)
    mtitle -- the movie title (optional)
    year -- the year the movie was released (optional)
    At least one of mid or mtitle must be passed as arguments

    Returns a dictionary of DataFrames, one for the 'movie' and another for the 'cast'.
    Where possible 'nested' dictionaries are "flattened" into columns with "dotted" names.
    Nested lists are kept as lists to be parsed later.
    If more than one movie is found with the given title, then the first one found is returned.

    Example calls:
    imdb_import_movie(mid='tt0115678')
    imdb_import_movie(mtitle='Big Night',year=1996)
    imdb_import_movie(mtitle='Big Night')

    """

    # make sure a movie has bee specified
    if (mid is None and mtitle is None):
        raise ValueError("Either mid or mtitle must be specified and cannot be blank")

    if (mid is not None):
        url= 'http://www.theimdbapi.org/api/movie?'+urllib.parse.urlencode({'movie_id':mid})
        try:
            imdb_movie = requests.get(url).json()
        except:
            # failed IMDB lookup
            raise ValueError("No movie with the given mid could be found")
    else:
        print(mtitle)
        qry = {'title':mtitle,'year':year} if year is not None and int(year)>1878 else {'title':mtitle}
        url = 'http://www.theimdbapi.org/api/find/movie?'+ urllib.parse.urlencode(qry)
        print(url)
        try:
            imdb_movie = requests.get(url).json()[0] # always use the first movie found
        except:
            # failed IMDB lookup
            raise ValueError("No movie with the given mtitle could be found")

    cast = pd.DataFrame(imdb_movie['cast'])
    del imdb_movie['cast']
    movie = json_normalize(imdb_movie)

    return {'movie':movie,'cast':cast}

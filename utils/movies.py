# -*- coding: utf-8 -*-
"""
Created on Fri May 15 17:04:29 2020

@author: Luther Ollier


_________________________________Movies utils function_________________________________
"""

import pandas as pd 

#I renamed the function movies to give a template for potential differents items to be recommend (ex : books)
#If we want to recommend another types of items, we only need to create a new file with the corresponding functions

#The best would be to create an abstract class items and then the class movies but I runned out of time

def get_item_id(movies, title, year=None):
    res = movies[movies['title'] == title]
    if year:
        res = res[res['year'] == year]

    if len(res) > 1:
        print("Ambiguous: found")
        print(f"{res['title']} {res['year']}")
    elif len(res) == 0:
        print('not found')
    else:
        return res.index[0]

def get_item_name(movies, index):
    return movies.iloc[index].title

def get_item_year(movies, index):
    return movies.iloc[index].year

def get_item_cat():
    return ["Animation", "Children's", 
       'Comedy', 'Adventure', 'Fantasy', 'Romance', 'Drama',
       'Action', 'Crime', 'Thriller', 'Horror', 'Sci-Fi', 'Documentary', 'War',
       'Musical', 'Mystery', 'Film-Noir', 'Western']

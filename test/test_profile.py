import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
import os

import sys
sys.path.append(sys.path[0][:len(sys.path[0])-5])
from similarity.similarity_profile import *

path=r'path to data'
path=r'C:/Users/luthe/Documents/AI/Tinyclues_test/Tinyclues_recommandation_algorithm/data'

items_filename='movies.csv'
ratings_filename='ratings.csv'
users_filename='users.csv'

items_path=os.path.join(path, items_filename)
ratings_path=os.path.join(path, ratings_filename)
users_path=os.path.join(path, users_filename)

items=pd.read_csv(items_path)
ratings=pd.read_csv(ratings_path)
users=pd.read_csv(users_path)

item_keys='movie_id'

test=Recommendation_profile(items, users, ratings, categories=get_item_cat(), item_keys=item_keys, user_keys='user_id')
user_id=np.random.randint(0,len(users))
test.get_recommendations(user_id)

if len(test.get_recommendations(np.random.randint(0,len(items))))!=5:
    raise 'error'
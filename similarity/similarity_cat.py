"""
This file contains the class Recommendation based on the items' categories
"""

### Import    
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import sys
sys.path.append(sys.path[0][:len(sys.path[0])-19])

### Depending of the item we want to recommend we might want to use other files, see movies.py for more details.
from utils.movies import *
from similarity.similarity import Recommendation


### this type of Recommandation is based on the item's categories
class Recommendation_cat(Recommendation):
    
    def __init__(self, items, users, ratings, categories:list, item_keys):
        Recommendation.__init__(self, items, users, ratings, item_keys)
        self.categories=categories
        self.similarity_matrix=self.__similarity_matrix__()
        
    def __similarity_matrix__(self):
        similarity_matrix = self.items[self.categories].values.dot(self.items[self.categories].values.T)
        return similarity_matrix
        
    def get_most_similar(self, item_id, top=10):
        best = self.similarity_matrix[item_id].argsort()[::-1]
        return [(ind, get_item_name(self.items, ind), self.similarity_matrix[item_id, ind]) for ind in best[:top] if ind != item_id]

    
    def get_recommendations(self, user_id, top=10):
        top_items_id = self.ratings[self.ratings['user_id'] == user_id].sort_values(by='rating', ascending=False).head(3)[self.item_keys]
        index=[self.item_keys, 'title', 'similarity']
        most_similars = []
        for top_item_id in top_items_id:
            most_similars += self.get_most_similar(top_item_id, top=top)
        return pd.DataFrame(most_similars, columns=index).drop_duplicates().sort_values(by='similarity', ascending=False).head(5)
"""
This file contains the abstract class Recommendation 
"""
### Import  
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

### the abstract class for different recommendations 
class Recommendation(ABC) :
    
    def __init__(self, items : pd.DataFrame, users : pd.DataFrame, ratings : pd.DataFrame, item_keys):
        
        self.items=items
        self.users=users
        self.ratings=ratings
        self.item_keys=item_keys

    @abstractmethod
    def __similarity_matrix__(self):
        #this function build the matrix of the metric we use to recommend the items.
        pass

    @abstractmethod
    def get_most_similar(self, items_id):
        #this function get the most similar items given a specific item
        pass
        
    @abstractmethod
    def get_recommendations(self, user_id):
        #this function get the recommendations for a given user
        pass
    
    

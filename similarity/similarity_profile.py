import sys
sys.path.append(sys.path[0][:len(sys.path[0])-5])
from similarity.similarity import *
from utils.movies import *

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans


class Recommendation_profile(Recommendation):
    
    def __init__(self, items, users, ratings, categories:list, item_keys, user_keys):
        
        Recommendation.__init__(self, items, users, ratings, item_keys)
        self.user_keys=user_keys
        self.users['profile']=self.__create_profiles__()
        self.categories=categories
        self.items['profile']=self.__items_profiles__()
        self.similarity_matrix=self.__similarity_matrix__()
        
    def __create_profiles__(self):
        x=np.zeros(self.users.shape)
        x=np.delete(x,0,1)
        i=0
        #this is the wrong way to implement it in order to scale it but I didn't have the time to correct if
        for column in self.users.columns:
            if self.users[column].nunique()!=len(self.users[column]):
                lb=LabelEncoder().fit(self.users[column].unique())
                x[:,i]=lb.transform(self.users[column].values)
                i+=1                
        sc=StandardScaler()
        x=sc.fit_transform(x)
        y=KMeans(n_clusters=5, random_state=0).fit_predict(x)
        return y
    
    def __items_profiles__(self):
        #we associate to each film the profile that watched it the most
        temp=pd.merge(self.ratings,self.users[[self.user_keys,'profile']])
        temp_pivoted=pd.pivot_table(temp, values='rating', index=self.item_keys, columns='profile', aggfunc=len)
        temp_pivoted['profile']=temp_pivoted.apply(pd.Series.argmax, axis=1)
        return temp_pivoted['profile']
    
    def __similarity_matrix__(self):
        #we consider the same matrix as the other method and another
        cat_matrix = self.items[self.categories].values.dot(self.items[self.categories].values.T)
        #and another matrix containing 1 if two films have the same user's profile type or 0 if not.
        commun_profiles_matrix=pd.get_dummies(self.items['profile']).values.dot(pd.get_dummies(self.items['profile'].values).T)
        
        #we add a point for the same profile type films.
        similarity_matrix=cat_matrix+commun_profiles_matrix 
        return similarity_matrix
        

    def get_most_similar(self, item_id, top=10):
        best =self.similarity_matrix[item_id].argsort()[::-1]
        return [(ind, get_item_name(self.items, ind), self.similarity_matrix[item_id, ind]) for ind in best[:top] if ind != item_id]
        
    def get_recommendations(self, user_id, top=10):
        top_items_id = self.ratings[self.ratings['user_id'] == user_id].sort_values(by='rating', ascending=False).head(3)[self.item_keys]
        index=[self.item_keys, 'title', 'similarity']
        most_similars = []
        for top_item_id in top_items_id:
            most_similars += self.get_most_similar(top_item_id, top=top)
        return pd.DataFrame(most_similars, columns=index).drop_duplicates().sort_values(by='similarity', ascending=False).head(5)
    
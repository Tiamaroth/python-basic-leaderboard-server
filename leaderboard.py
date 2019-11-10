import operator

class Leaderboard:
    """
        Low-level leaderboard classes. Handles users' storage, update and sort.    
    """

    def __init__(self):
        self.users_dict = {}
        self.has_changed = False # Whether or not the cache has been invalidated
        self.sorted_list = [] # Cached response

    def insert_user_or_update_user_score(self,user):
        self.users_dict[user['user']] = user #As in pure python json serialization is not straightforward, i'll keep using strings
        self.has_changed = True
        
    
    def update_user_score(self, user):
       self.users_dict[user['user']]['score'] += int(user['score']) 
       self.has_changed = True

    def get_top(self,number):
        self.sort()
        return self.sorted_list[:number]

    def get_partial(self,middle,range):
        self.sort()
        middle -= 1
        top = max(min(middle+range,len(self.users_dict)),0)+1
        bot = max(min(middle-range,len(self.users_dict)),0)  
        return self.sorted_list[bot:top]    

    def sort(self):
        """
            Sorts the users' list in-place and stores it in the cache reply.
            Does nothing if the cache is still valid, so this can safely be called multiple times.
        """
        if self.has_changed:
            self.sorted_list = sorted(self.users_dict.values(), key=operator.itemgetter("score", "user"), reverse=True)
            self.has_changed = False
    
    def has_user(self, user_id):
        return user_id in self.users_dict 
    
    def clear(self):
        self.users_dict.clear()
        self.has_changed = True

    


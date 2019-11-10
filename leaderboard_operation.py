from leaderboard import Leaderboard
import json
from exceptions import RequestError

class LeaderboardOperations:
    """
        Proxy class between HTTP requests (see request_handler.RequestHandler) and leaderboard.Leaderboard.
        Parses the request and forwards it.
    """
    
    kStatus_ok = {"status":"OK"}
    kStatus_ko = {"status":"KO"}
    
    
    def __init__(self):
        self.leaderboard = Leaderboard()

    def get_top(self, path):
        """
            Retrieve top XX of the leaderboard
        """        
        top_number = path.rsplit('/', 1).pop()
        try:
            sorted_list = self.leaderboard.get_top(int(top_number)) #TODO refactor
            return JSONResponse(200,sorted_list)
        except ValueError:
            raise RequestError(400,"Wrong parameter type expected int got {}".format(top_number))

    def get_partial(self, path):
        """
            Retrieve relative ranking around a position 
        """
        splitted = path.rsplit('/', 2)
        try:
            sorted_list = self.leaderboard.get_partial(int(splitted[1]),int(splitted[2])) #TODO sanity check
            return JSONResponse(200,sorted_list)
        except ValueError:
            raise RequestError(400,"Wrong parameter type expected int got {}".format(splitted))

    def insert_or_update(self,parsed_req):
        """
            As updating a score in absolute "in this case" is equivalent to creating a new user we don't need separated operations
        """
        self.leaderboard.insert_user_or_update_user_score(parsed_req)
        return JSONResponse(200,self.kStatus_ok)
    
    def update(self,parsed_req):
        """
            Update the score of a specific user ,if exists otherwise rise RequestError
        """
        if not self.leaderboard.has_user(parsed_req['user']):
            raise RequestError(404, "User {} does not exist".format(parsed_req['user']))

        self.leaderboard.update_user_score(parsed_req)
        return JSONResponse(200,self.kStatus_ok)



class JSONResponse:
    """
        Helper class to return JSON-formatted responses
    """
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = json.dumps(body).encode('utf-8')

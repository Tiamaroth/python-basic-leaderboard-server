from http.server import BaseHTTPRequestHandler
from leaderboard import LeaderboardFirst
import json


class Server(BaseHTTPRequestHandler):

    
    leaderboard = LeaderboardFirst()
    status_ok = {"status":"OK"}
    status_ko = {"status":"KO"}

    def do_POST(self):
        #here we read content of post
        length = int(self.headers['content-length'])
        #split depending on path
        if '/update/user/absolute' == self.path:
            parsed_req = json.loads(self.rfile.read(length).decode('utf-8'))
            if  len(parsed_req) != 2 or not isinstance(parsed_req.get('score'),int) or not isinstance(parsed_req.get('user'),int): #checks that it exists and is of type int
                self.do_reply(400,self.status_ko)
            else:
                self.do_insert_or_update(parsed_req)
        elif '/update/user/relative' == self.path:
            parsed_req = json.loads(self.rfile.read(length).decode('utf-8'))
            if  len(parsed_req) != 2 or not isinstance(parsed_req.get('score'),str) or not isinstance(parsed_req.get('user'),int): #checks that it exists and is of type int
                self.do_reply(400,self.status_ko)
            else:    
                self.do_update(parsed_req)
        else:
            self.do_reply(404,self.status_ko)
        
    def do_GET(self):
        if self.path.startswith("/top/"):
            self.do_top()
        elif self.path.startswith("/partial/"):
            self.do_partial()
        else:
            self.do_reply(404,self.status_ko)
        
        
    
    def do_top(self):
        """
            Retrieve top XX of the leaderboard
        """
        if self.path.count('/') != 2:
            self.do_reply(400,self.status_ko)
        else:
            top_number = self.path.rsplit('/', 1).pop()
            try:
                sorted_list = self.leaderboard.get_top(int(top_number)) #TODO refactor
                self.do_reply(200,sorted_list)
            except ValueError:
                self.do_reply(400,self.status_ko)

    def do_partial(self):
        """
            Retrieve relative ranking around a position 
        """
        if self.path.count('/') != 3:
            self.do_reply(400,self.status_ko)
        else:
            splitted = self.path.rsplit('/', 2)
            try:
                sorted_list = self.leaderboard.get_partial(int(splitted[1]),int(splitted[2])) #TODO sanity check
                self.do_reply(200,sorted_list)
            except ValueError:
                self.do_reply(400,self.status_ko)

    def do_insert_or_update(self,parsed_req):
        """
            As updating a score in absolute "in this case" is equivalent to creating a new user we don't need separated operations
        """
        self.leaderboard.insert_user_or_update_user_score(parsed_req)
        self.do_reply(200,self.status_ok)
    
    def do_update(self,parsed_req):
        """
            Update the score of a specific user
        """
        if self.leaderboard.has_user(parsed_req['user']):
            self.leaderboard.update_user_score(parsed_req)
            self.do_reply(200,self.status_ok)
        else:
            self.do_reply(404,self.status_ko)
    
    def do_reply(self,httpstatus,write):
        """
            Perform the reply to client
        """
        self.send_response(httpstatus)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(write).encode('utf-8'))     
        


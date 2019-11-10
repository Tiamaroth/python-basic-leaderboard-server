import unittest
import sys
sys.path.append("..")
import request_handler
import leaderboard_operation
import urllib.request
import json
import threading
from http.server import HTTPServer
import time
import random
SERVER_PORT = 8081
server_url = "http://localhost:%s" % SERVER_PORT

class TestBase(unittest.TestCase):

    jsonHeader = {'content-type': 'application/json'}

    test_thread = None
    
    def setUp(self):
        httpd = HTTPServer(("localhost", SERVER_PORT), request_handler.RequestHandler)
        httpd.timeout = 0.1
        print(time.asctime(), 'Test Server UP - ')
        self.server_alive = True
        def run_server():
            while self.server_alive:
                httpd.handle_request()
            httpd.server_close()
        self.test_thread = threading.Thread(target=run_server)
        self.test_thread.start()   

    def tearDown(self):
        request_handler.RequestHandler.leaderboard_operation.leaderboard.clear()
        self.server_alive = False
        self.test_thread.join()
        print(time.asctime(), 'Test Server DOWN - ')


    def send_http_get(self,address):
        """ 
            Perform an http get on :address
        """
        with urllib.request.urlopen(address) as f:
            return f.read()
    def send_http_get_deserialized(self,address):
        """ 
            Perform an http get on :address and return already deserialized 
        """
        return json.loads(self.send_http_get(address).decode("utf-8"))

    def send_http_post(self,address,data):
        """
            Perform an http get on :address with :data
        """
        params = json.dumps(data).encode('utf-8')
        #adding data params will switch automatically to POST
        req = urllib.request.Request(address, data=params, headers=self.jsonHeader) 
        with urllib.request.urlopen(req) as f:
            self.assertEqual(json.loads(f.read().decode("utf-8")), leaderboard_operation.LeaderboardOperations.kStatus_ok)
             
    
    def add_X_user(self,num_user):
        """
            Generate :num_user users
        """
        generated_users = []
        for i in range(1,num_user+1):
            generated_users.append({'user': i, 'score': random.randint(1,1000)})
        
        return generated_users
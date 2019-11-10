from http.server import BaseHTTPRequestHandler
from exceptions import RequestError
from leaderboard_operation import LeaderboardOperations
import json
import logging

class RequestHandler(BaseHTTPRequestHandler):
    """
        Request handler for python's http.server.
        Describes what should be done when an HTTP request is received.
        Performs pre-checks using the RequestChecks class and forwards it to LeaderboardOperations.
    """

    leaderboard_operation = LeaderboardOperations()
    kGet_top_params = 2
    kGet_partial_params = 3 
    kAbsolute_schema ={'user' : int, 'score': int}
    kRelative_schema ={'user' : int, 'score': str}

    def do_POST(self):
        try:           
            length = int(self.headers['content-length'])
            if '/update/user/absolute' == self.path:
                parsed_req = json.loads(self.rfile.read(length).decode('utf-8'))
                RequestChecks.check_schema(self.kAbsolute_schema,parsed_req)
                response = self.leaderboard_operation.insert_or_update(parsed_req)
            elif '/update/user/relative' == self.path:
                parsed_req = json.loads(self.rfile.read(length).decode('utf-8'))
                RequestChecks.check_schema(self.kRelative_schema,parsed_req)
                response = self.leaderboard_operation.update(parsed_req)
            else:
               raise RequestError(404, "Resource {} does not exist".format(self.path))
            self.do_reply(response.status_code, response.body)
        except RequestError as e:
            self.do_reply(e.status_code, e.message)
        except json.JSONDecodeError:
            self.do_reply(400, b"Body was not JSON, please send data in JSON format")
        except Exception as e: # pragma: no cover
            # Catching Exception is frowned upon in python, but as we need to catch any remaining exception to actually send a reply to the client,
            # otherwise they will end up with a weird error such as "EMPTY RESPONSE".
            # Any exception landing here should be considered a bug.
            logging.exception("Got exception in POST")
            self.do_reply(500, b'Internal server error, please report')
        
    def do_GET(self):
        """
            Handles any GET request.
            Note: by choice, we do not handle GET parameters (?key=val&key2=val2) at all. This allows for prettier URLs.
        """
        try:
            if self.path.startswith("/top/"):
               RequestChecks.check_get_route(self.path, self.kGet_top_params)
               response = self.leaderboard_operation.get_top(self.path)
            elif self.path.startswith("/partial/"):
               RequestChecks.check_get_route(self.path,self.kGet_partial_params)
               response = self.leaderboard_operation.get_partial(self.path)
            else:
                raise RequestError(404, "Resource {} does not exist".format(self.path))
            self.do_reply(response.status_code, response.body)
        except RequestError as e:
            self.do_reply(e.status_code, e.message)
        except Exception as e: # pragma: no cover
            # Catching Exception is frowned upon in python, but as we need to catch any remaining exception to actually send a reply to the client,
            # otherwise they will end up with a weird error such as "EMPTY RESPONSE".
            # Any exception landing here should be considered a bug.
            logging.exception("Got exception in GET")
            self.do_reply(500, b'Internal server error, please report')                
    
    def do_reply(self, status, body):
        """
            Fill the client reply with an HTTP status and a body.
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(body)


class RequestChecks:
    """
        Pre-checks needed before forwarding queries to LeaderboardOperations.
    """
    
    @staticmethod
    def check_schema(reference_schema, parsed_req):
        """
            Checks that parsed_req content is compliant to reference_schema. E.g. :parsed_req['user'] is a str, no extraneous parameters. 
            Raise RequestError if it's not.
        """
        for key in reference_schema:
            if key not in parsed_req:
                raise RequestError(400, "Missing parameter {}".format(key))
            if not isinstance(parsed_req[key],reference_schema[key]):
                raise RequestError(400, "Bad parameter type for parameter {}, got {} but expected {}".format(key, type(parsed_req[key]).__name__, reference_schema[key].__name__))
        if len(parsed_req) != len(reference_schema):
                raise RequestError(400, "Unexpected number of parameters, got {} but expected {}".format(len(parsed_req), len(reference_schema)))

    @staticmethod            
    def check_get_route(path, expected_len):
        """
            Check if current path has expected number of params 
            eg. '/get/100/2' <-> param_len == 2
        """
        if path.count('/') != expected_len:
            raise RequestError(400, "Unexpected number of parameters, got {} but expected {}".format(path.count('/'), expected_len))
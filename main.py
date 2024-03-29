import time
from http.server import HTTPServer
from request_handler import RequestHandler

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8080

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), RequestHandler)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))
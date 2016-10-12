from wsgiref.simple_server import make_server
from wsgi_application import WSGIApplication

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8080
    server = make_server(ip, port, WSGIApplication)
    print('Serving on port {}'.format(port))
    server.serve_forever()
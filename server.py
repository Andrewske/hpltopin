from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

httpd = HTTPServer(('localhost', 4443), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(httpd.socket, keyfile = 'https/rootCA.key', certfile='https/rootCA.cert', server_side=True)
httpd.serve_forever()
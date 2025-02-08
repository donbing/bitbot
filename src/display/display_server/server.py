#!/usr/bin/env python3

from http.server import HTTPServer
from handlers import InkyHandler

# start the webserver
server = HTTPServer(('', 8081), InkyHandler)
server.serve_forever()

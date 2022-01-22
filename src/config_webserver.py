import pathlib
import os
import os.path
from os.path import join as pjoin
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse as urlparse

curdir = pathlib.Path(__file__).parent.resolve()
config_folder = pjoin(curdir, '../config/') 

files = {
    "config_ini": pjoin(config_folder, 'config.ini'),
    "log_output": pjoin(curdir, '../', 'debug.log'),
    "base_style": pjoin(config_folder, 'base.mplstyle'),
    "inset_style": pjoin(config_folder, 'inset.mplstyle'),
    "default_style": pjoin(config_folder, 'default.mplstyle'),
    "volume_style": pjoin(config_folder, 'volume.mplstyle') 
}

class StoreHandler(BaseHTTPRequestHandler):

    def create_editor_form(self, fileKey, current_file_key):
        with open(files[fileKey]) as file_handle:
            html =  '<h2 class="collapser">⚙️ ' + fileKey + '</h2>'
            html += '<form method="post" action="?fileKey=' + fileKey + '"' + ' class="' + ('open' if fileKey == current_file_key else '') + '">'
            html += '<textarea name="fileContent" rows="20" cols="80">' + str(file_handle.read()) + '</textarea>'
            html += '<div><input type="submit" value="Save"></input></div></form>'
            return html

    def do_GET(self):
        param = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('fileKey',[])
        fileKey = next((x for x in param), None)
        # html for config editor
        html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
                <meta content="utf-8" http-equiv="encoding">
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
                <style>
                    form { display: none; }
                    form.open { display:block; }
                    .collapser { cursor: pointer; }
                </style>
                <script>
                    window.onload= function(){
                        var coll = document.getElementsByClassName("collapser");
                        for (var i = 0; i < coll.length; i++) {
                            coll[i].addEventListener("click", function() {
                                    var content = this.nextElementSibling;
                                content.style.display = content.style.display === "block" ? "none" : "block";
                            });
                        }
                    }
                </script>
            </head>
            <body>
                <h1>🤖 BitBot Crypto-Ticker Config</h1>
            '''
        html+=self.create_editor_form("config_ini", fileKey)
        html+=self.create_editor_form("base_style", fileKey)
        html+=self.create_editor_form("inset_style", fileKey)
        html+=self.create_editor_form("default_style", fileKey)
        html+=self.create_editor_form("volume_style", fileKey)

        # display log info if it exists
        if os.path.isfile(files['log_output']):
            with open(files['log_output']) as log_file:
                html += '<h1 class="collapser">🪵 LOG</h1><textarea name="configfile" rows="20" cols="80">' + str(log_file.read()) + '</textarea>'

        html += '''
            </body>
            </html>
                '''
        # html response
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))

    def do_POST(self):
        fileKey = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('fileKey', None)[0]
        # form vars
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'})

        # write config file to disk
        with open(files[fileKey], 'w') as fh:
            fh.write(form.getvalue('fileContent'))

        # redirect to get action
        self.send_response(302)
        self.send_header('Location', self.path)
        self.end_headers()

# start the webserver
server = HTTPServer(('', 8080), StoreHandler)
server.serve_forever()
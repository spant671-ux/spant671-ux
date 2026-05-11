import http.server
import socketserver
import urllib.parse
import urllib.request
import json
import base64
import sys

CLIENT_ID = "df465593fad147dcbc4040d8bdb9bbcc"
CLIENT_SECRET = "81cf410046294dcebf1c15287e7a9207"
REDIRECT_URI = "http://localhost:8080"

class SpotifyAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        if 'code' in params:
            code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Success! You can close this window and return to the chat.</h1>")
            
            # Exchange code for refresh token
            auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
            data = urllib.parse.urlencode({
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': REDIRECT_URI
            }).encode()
            
            req = urllib.request.Request("https://accounts.spotify.com/api/token", data=data)
            req.add_header("Authorization", f"Basic {auth_header}")
            
            try:
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read())
                    print("\n\n=== SPOTIFY TOKENS ===")
                    print(f"SPOTIFY_REFRESH_TOKEN: {res_data.get('refresh_token')}")
                    print("======================\n\n")
            except Exception as e:
                print("Error exchanging token:", e)
                
            # Exit server after successful fetch
            sys.exit(0)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code found.")

if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), SpotifyAuthHandler) as httpd:
        print(f"Serving at port {PORT}. Waiting for callback...")
        httpd.serve_forever()

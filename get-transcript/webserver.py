from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import get_transcript as gt
import webbrowser as wb

# this file:
# 1) runs localhost:8080 in a separate thread
# 2) opens the OAuth site to get the authorization code
# 3) retrieves the transcript after authorization (no longer need run-get-transcript.py)

# problem (limitation?): must be signed in to Zoom account online BEFORE running

spongebob = gt.Transcript(meeting_id=None,  # global Transcript object, kinda awkward
                          client_key=None,
                          client_secret=None,
                          code=None)


class echoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(self.path.encode())
        query_components = parse_qs(urlparse(self.path).query)
        if 'code' in query_components and spongebob.code is None:
            spongebob.code = query_components['code'][0]
            spongebob.GetTranscript()


def run():
    PORT = 8080
    server = HTTPServer(('', PORT), echoHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()


def run_thread():
    t = threading.Thread(target=run)
    t.start()


def serve_transcript(meeting_id, client_key, client_secret):
    spongebob.meeting_id = meeting_id
    spongebob.client_key = client_key
    spongebob.client_secret = client_secret

    run_thread()

    url = "zoom.us/oauth/token?response_type=code&client_id={0}&redirect_uri=http://localhost:8080".format(
        spongebob.client_key)

    # MacOS
    # chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

    # Windows
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    edge_path = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s'

    # Linux
    # chrome_path = '/usr/bin/google-chrome %s'

    wb.get(edge_path).open(url)


# serve_transcript(94923151321, "FEc1Rq0JTi2MFfHNH94DgA", "WECczlqk1PZLmmwzt1c1n43hcmw7lHDJ")

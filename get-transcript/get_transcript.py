import base64
import http.client
import json
import requests

# url used to get the code that's used to get OAuth access token
# zoom.us/oauth/token?response_type=code&client_id=FEc1Rq0JTi2MFfHNH94DgA&redirect_uri=http://localhost:8080
# redirect_url must be whitelisted when you create the app

# use case: Transcript(meeting_id, access_token).GetTranscript()
#   or Transcript(meeting_id, client_key, client_secret, code).GetTranscript()

class Transcript():
    """Use the API token's key, secret, and code to get transcript file from cloud recording of meeting with id meeting_id."""
    
    def __init__(self, meeting_id, client_key=None, client_secret=None, code=None, access_token=None):
        """
        Args: 
            client_key (string): Key of api token.
            client_secret (string): Secret of api token.
            code (string): Code created when directed to OAuth URL.
            meeting_id (integer): ID of the meeting you need the transcript for.
        """
        self.meeting_id = meeting_id
        self.client_key = client_key
        self.client_secret = client_secret
        self.code = code
        self.access_token = access_token
        self.conn = None

        self.start_date = None
        self.start_time = None
    
    def GetTranscript(self):
        """Gets the transcript using the paramters the instance has access to."""

        self.conn = http.client.HTTPSConnection("zoom.us")
        got_file = False
        if None in [self.client_key, self.client_secret, self.code] and self.access_token is None:
            print("Zoom OAuth token needed to get transcript.")
            return got_file

        if self.access_token is None:
            self.access_token = self._GetAccessToken()

        try:
            download_url = self._GetDownloadUrl()
        except:
            print("Bad Access Token")
            if None in [self.client_key, self.client_secret, self.code]:
                print("client_key, client_secret, and code needed to create access token.")
                return got_file
            self.access_token = self._GetAccessToken()
            download_url = self._GetDownloadUrl()
        
        if download_url is None:
            print("Meeting Not Found.")
        else:
            transcript = requests.get(download_url, allow_redirects=True)
            open("{meeting_id}_audio_transcript.vtt".format(meeting_id=self.meeting_id), 'wb').write(transcript.content)
            got_file = True

        f = open("{meeting_id}_times.txt".format(meeting_id=self.meeting_id), "w+")
        f.write("{0} \n".format(self.start_date))
        f.write("{0}GMT \n".format(self.start_time))
        return got_file

    def _GetAccessToken(self):
        """Gets an access token using client_key, client_secret, and code."""

        # Encoding client authorization 
        pair = "{client_key}:{client_secret}".format(client_key=self.client_key, client_secret=self.client_secret)
        # authorization = base64.b64encode(pair) -- python2
        authorization = base64.b64encode(str(pair).encode("utf-8")).decode("utf-8")

        # Getting the access token
        access_token_headers = { "Authorization": "Basic {authorization}".format(authorization=authorization) }
        request_endpoint = "/oauth/token?grant_type=authorization_code&code={code}&redirect_uri=http://localhost:8080".format(code=self.code)
        self.conn.request("POST", request_endpoint, headers=access_token_headers)
        res = self.conn.getresponse()
        response = json.loads(res.read().decode("utf-8"))

        try:
            return response["access_token"]
        except KeyError:
            print("Request for access token failed for the following reason: {reason}".format(reason=response["reason"]))
    
    def _GetDownloadUrl(self):
        """Gets the url needed to downaload the transcript."""

        # Using access_token to get the transcript for the meeting that's mapped to meeting_id
        get_meeting_headers = {
            'authorization': "Bearer {access_token}".format(access_token=self.access_token),
            'content-type': "application/json"
        }
        # Get a list of all meetings
        # for some reason, only getting meetings from the past month? (update: max range = 1 month!)
        try:
            # request_endpoint = "/v2/users/me/recordings?from=2000-01-01" --> Dave's version
            request_endpoint = "/v2/users/me/recordings?from=2020-11-22&to=2020-11-24" # specify date range
            self.conn.request("GET", request_endpoint, headers=get_meeting_headers)
            res = self.conn.getresponse()
            data = res.read().decode("utf-8")
            response = json.loads(data)
            # print(response)  ## print statement to check date range
        except:
            print("Bad Response to access recordings.")
            print(data)
        
        # Download the transcript if it exists
        download_url = None
        for meeting in response["meetings"]:
            if "recording_files" not in meeting or meeting["id"] != self.meeting_id:
                continue
            for recording_file in meeting["recording_files"]:
                if "recording_type" not in recording_file:
                    continue
                if recording_file["file_type"] == "TRANSCRIPT":
                    time = meeting["start_time"]
                    self.start_date = time[0:10]
                    self.start_time = time[11:16]
                    download_url = "{endpoint}?access_token={access_token}".format(endpoint=str(recording_file["download_url"]), access_token=self.access_token)
        return download_url



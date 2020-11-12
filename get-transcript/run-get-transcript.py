import get_transcript as gt

# steps before running:
# 1) run localhost:8080 server
# 2) zoom.us/oauth/token?response_type=code&client_id=FEc1Rq0JTi2MFfHNH94DgA&redirect_uri=http://localhost:8080
# 3) make sure id, key, secret, and code all correct

# example meetingIDs: 92023192477 (07/31 Chemistry Expo, unreachable), 94923151321 (11/05 and 11/10!!!)

# limitations:
# 1) must update code before each run, instead of every hour, or is the hour just for the token?
# 2) only getting meetings from the last month

# (self, meeting_id, client_key=None, client_secret=None, code=None, access_token=None)
spongebob = gt.Transcript(meeting_id=94923151321, # J's 11/10 meeting
                          client_key="FEc1Rq0JTi2MFfHNH94DgA",
                          client_secret="WECczlqk1PZLmmwzt1c1n43hcmw7lHDJ",
                          code="bjc928tYW5_wcT7DtCgTKKr-HDFlXouZA") # update before each run

spongebob.GetTranscript()




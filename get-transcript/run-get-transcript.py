import get_transcript as gt

#(self, meeting_id, client_key=None, client_secret=None, code=None, access_token=None)
spongebob = gt.Transcript(meeting_id=98352037195,
                          client_key="FEc1Rq0JTi2MFfHNH94DgA",
                          client_secret="WECczlqk1PZLmmwzt1c1n43hcmw7lHDJ",
                          code="4evXGbJlwR_wcT7DtCgTKKr-HDFlXouZA")

#spongebob._GetAccessToken()

spongebob.GetTranscript()




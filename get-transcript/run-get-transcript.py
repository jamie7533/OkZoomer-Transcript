import get_transcript as gt

#(self, meeting_id, client_key=None, client_secret=None, code=None, access_token=None)
spongebob = gt.Transcript(meeting_id=92023192477,
                          client_key="BKhl0JRRQIGKu3YW8yzXeg",
                          client_secret="udT4tQdPTgCE4lvqwUElrBVUMP9HGJxc",
                          code="fR5lny4Uhl_wcT7DtCgTKKr-HDFlXouZA")

#spongebob._GetAccessToken()

spongebob.GetTranscript()




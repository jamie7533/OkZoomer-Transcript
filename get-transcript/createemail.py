import smtplib, ssl
import matplotlib.pyplot as plt
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import get_breakdown as gb
import webserver as wb

#information for report

# names = ["Jamie", "Tony", "Nick", "Claudia"]
meeting_id = int(input("Type your meeting ID and press Enter: "))
wb.serve_transcript(meeting_id, client_key="FEc1Rq0JTi2MFfHNH94DgA", client_secret="WECczlqk1PZLmmwzt1c1n43hcmw7lHDJ")
while not os.path.exists("{0}_audio_transcript.vtt".format(meeting_id)):
    pass
breakdowns = gb.getBreakdown("{0}_audio_transcript.vtt".format(meeting_id))
total_seconds = 0
seconds = []
names = []
positive = "Positive: "
negative = "Negative: "
for b in breakdowns:
    total_seconds += b[1]
    names.append(b[0])
    seconds.append(b[1])
    if b[2]== 'Positive':
        positive = positive + " " + b[0] + ","
    elif b[2]== 'Negative':
        negative = negative + " " + b[0] + ","
    
numpersons = len(names)
meeting_id = str(meeting_id)

if positive == "Positive: ":
    positive = ""
else:
    positive = positive[0:len(positive)-1]
if negative == "Negative: ":
    negative = ""
else:
    negative = negative[0:len(negative)-1]

sentiment = "Using Sentiment Analysis Powered by MonkeyLearn we noticed the following people stood out:"

percentages = [int(s / total_seconds * 100) for s in seconds]
stringnames = ', '.join(names)
# percentages = [25, 25, 30, 20]
#percentages = [10, 40, 25, 25]
meetingdate = "11/10/2020"
meetingtime = "5:30pm"

#analyzing times
generalremark = "Well done! Everyone spoke equally during this meeting. Keep it up!"
remarkcolor="#19B953"
idealtime = 100/numpersons
for i in percentages:
    if i < idealtime - 5 or i > idealtime + 5:
        generalremark = "Next time, make sure everyone gets to contribute equally to the conversation! \n Please review the chart to see how you can improve in the next meeting."
        remarkcolor = "#E37100"


#email set up
sender_email = "okzoomerteam@gmail.com"
receiver_email = input("Type your email and press enter:")
password = "Evanston1" #input("Type your password and press enter:")

message = MIMEMultipart()
message["Subject"] = "Summary of Your Meeting"
message["From"] = sender_email
message["To"] = receiver_email


#create pie chart
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = names
sizes = percentages
explode = [0 for i in range(numpersons)] # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.savefig('piechart.png', bbox_inches='tight')

#attaching image
img_data = open("piechart.png", 'rb').read()
image = MIMEImage(img_data, name=os.path.basename("piechart.png"))
message.attach(image)


# Create the plain-text and HTML version of your message
html = """\
<html>
    <h1 style="text-align: center;">Your Meeting Summary</h1>
    <h2 style ="text-align: center;">For meeting <span style="color:#A53FD2; text-align: center;">{0}</span> on 
    <span style="color:#A53FD2;">{1}</span> at <span style="color:#A53FD2;">{2}</span> </h2>
    <h3 style="text-align: center;"> Meeting attendees: <span style="color:#12A5D5"> {3} </span></h3>
    <h3 style ="color:{5}; text-align: center;"> {4} </h3>
    <h3 style ="color:#17B50E; text-align: center;"> {6} </h3>
    <h3 style ="color:#17B50E; text-align: center;"> {7} </h3>
    <h3 style ="color:#17B50E; text-align: center;"> {8} </h3>
    <img src="piechart.png"></img>

    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
  

</html>
""".format(meeting_id, meetingdate, meetingtime, stringnames, generalremark, remarkcolor, sentiment, positive, negative)



# # Turn these into plain/html MIMEText objects
#part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# # Add HTML/plain-text parts to MIMEMultipart message
# # The email client will try to render the last part first
#message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

print("sent")
import smtplib, ssl
import matplotlib.pyplot as plt
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import get_breakdown as gb

#information for report
numpersons = 4
names = ["Jamie", "Tony", "Nick", "Claudia"]
stringnames = ', '.join(names)
percentages = [25, 25, 30, 20]
#percentages = [10, 40, 25, 25]
meetingid = "6102983"
meetingdate = "20/10/2020"
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
receiver_email = "okzoomerteam@gmail.com"
password = "Evanston1" #input("Type your password and press enter:")

message = MIMEMultipart()
message["Subject"] = "Summary of Your Meeting"
message["From"] = sender_email
message["To"] = receiver_email


#create pie chart
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = names
sizes = percentages
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

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
    <img src="piechart.png"></img>

    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
  

</html>
""".format(meetingid, meetingdate, meetingtime, stringnames, generalremark, remarkcolor)



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
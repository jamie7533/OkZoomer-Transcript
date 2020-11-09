import smtplib, ssl
import matplotlib.pyplot as plt
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

sender_email = "okzoomerteam@gmail.com"
receiver_email = "okzoomerteam@gmail.com"
password = "Evanston1" #input("Type your password and press enter:")

message = MIMEMultipart("alternative")
message["Subject"] = "Test 2"
message["From"] = sender_email
message["To"] = receiver_email

#information for report
numpersons = 4
names = ["Jamie", "Tony", "Nick", "Claudia"]
percentages = [25, 25, 30, 20]
meetingid = "6102983"
meetingdate = "20/10/2020"
meetingtime = "5:30pm"

#attaching image
img_data = open("testphoto.png", 'rb').read()
image = MIMEImage(img_data, name=os.path.basename("testphoto.png"))
message.attach(image)

# Create the plain-text and HTML version of your message
text = meetingid
html = """\
<html>
    <h1>Your Meeting Summary</h1>
    <h2>For meeting {0}</h2> 

    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    .pie {{
            width:400px; 
            height: 400px; 
            background-color: red;
            border-radius: 50%
            )


    }}
    </style>
    </head>
    <body>

    <h2>Square CSS</h2>
    <div class="square"></div>

    </body>
    <head> 
        <meta charset="UTF-8"> 
        <meta name="viewport" content= 
            "width=device-width, initial-scale=1.0"> 
    
        <title>Pie Chart</title> 
    
        <style> 
            .piechart {{
            width: 400px; 
            height: 400px; 
            border-radius: 50%; 
            background-color: purple; 
            }} 
    
        </style> 
    </head> 
    
    <body> 
        <h1>Pie Chart</h1> 
        <div class="piechart"></div> 
    </body> 
  

</html>
""".format(meetingid)



# # Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# # Add HTML/plain-text parts to MIMEMultipart message
# # The email client will try to render the last part first
#message.attach(part1)
#message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
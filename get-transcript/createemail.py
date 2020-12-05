import smtplib, ssl
import matplotlib.pyplot as plt
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import get_breakdown as gb
import webserver as wb


def email(id, email):
    meeting_id = int(id)
    wb.serve_transcript(meeting_id, client_key="FEc1Rq0JTi2MFfHNH94DgA", client_secret="WECczlqk1PZLmmwzt1c1n43hcmw7lHDJ")

    while not os.path.exists("{0}_audio_transcript.vtt".format(meeting_id)):
        pass
    breakdowns = gb.getBreakdown("{0}_audio_transcript.vtt".format(meeting_id))
    time_file = open("{0}_times.txt".format(meeting_id))
    time_file_reader = time_file.readlines()
    meetingdate = time_file_reader[0]
    meetingtime = time_file_reader[1]

    total_seconds = 0
    seconds = []
    names = []
    positive = """<span style="font-weight:bold;">Positive: </span>"""
    negative = """<span style="font-weight:bold;">Negative: </span>"""
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

    sentiment = "Using Sentiment Analysis we noticed the following people stood out:"

    percentages = [int(s / total_seconds * 100) for s in seconds]
    stringnames = ', '.join(names)

    # analyzing times
    generalremark = "Well done! Everyone spoke equally during this meeting. Keep it up!"
    remarkcolor="#19B953"
    idealtime = 100/numpersons
    for i, v in enumerate(percentages):
        if v < idealtime - 5 or v > idealtime + 5:
            remarkcolor = "#E37100"
            if v < idealtime - 5:
                generalremark = """\
                Next time, make sure everyone gets to contribute equally to the conversation! <br>
                It looks like <span style="color:#E37100;">{quiet_person}</span> did not get to talk as much. <br><br>
                Please review the chart to see how you can improve in the next meeting.                
                """.format(quiet_person=names[i])
                break
            else:
                generalremark = "Next time, make sure everyone gets to contribute equally to the conversation! <br><br>" \
                                " Please review the chart to see how you can improve in the next meeting."


    # email set up
    sender_email = "okzoomerteam@gmail.com"
    # receiver_email = input("Type your email and press enter:")
    receiver_email = email
    password = "Evanston1"  # input("Type your password and press enter:")

    message = MIMEMultipart()
    message["Subject"] = "Summary of Your Meeting"
    message["From"] = sender_email
    message["To"] = receiver_email

    # remove old pie charts
    for filename in os.listdir('static'):
        if filename.startswith('pie'):
            os.remove('static/' + filename)
    # create pie chart
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    plt.switch_backend('Agg')
    labels = names
    sizes = percentages
    explode = [0 for i in range(numpersons)]  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.title("Participant Speaking Times")

    new_graph_name = "piechart" + str(time.time()) + ".png"  # eliminate cache problems

    plt.savefig('static/{new_graph}'.format(new_graph=new_graph_name), bbox_inches='tight')
 
    # attaching image
    img_data = open("static/{new_graph}".format(new_graph=new_graph_name), 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename(new_graph_name))
    message.attach(image)

    # Create the plain-text and HTML version of your message
    html2 = """\
    <html>
        <h1 style="text-align: center;">Your Meeting Summary</h1>
        <h2 style ="text-align: center;">For meeting <span style="color:#A53FD2; text-align: center;">{0}</span> on 
        <span style="color:#A53FD2;">{1}</span> at <span style="color:#A53FD2;">{2}</span> </h2>
        <h3 style="text-align: center; font-weight: normal"> Meeting attendees: <span style="color:black"> {3} </span></h3>
        <h3 style ="color:black; text-align: center;"> {6} </h3>
        <h3 style ="color:#17B50E; text-align: center;"> {7} </h3>
        <h3 style ="color:#E37100; text-align: center;"> {8} </h3>
        <h3 style ="color:black; text-align: center; padding-top: 10px"> Next time, make sure everyone contributes 
        equally to the conversation! It looks like Tony did not get to talk as much. <br>
        Please review the chart to see how you can improve in the next meeting. </h3>
        <img src="piechart.png"></img>

        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1"> """

    html = """\
    <html>    
       <h1 style="text-align: center">Your Meeting Summary</h1>
       <hr>
       <h2 style ="text-align: left;">For meeting <span style="color:#A53FD2; font-weight: normal">{0}</span> on
       <span style="color:#A53FD2; font-weight: normal">{1}</span> at <span style="color:#A53FD2;font-weight: normal">
             {2}</span> </h2>
       <h2 style="text-align: left;"> Attendees: <span style="color:black; font-weight: normal">
          {3} </span></h2>
       <hr>
       <h2 style ="color:black; text-align: left"> {6} </h2>
       <h3 style ="color:#17B50E; text-align: left; padding-left: 40px; font-weight: normal"> {7} </h3>
       <h3 style ="color:#E37100; text-align: left; padding-left: 40px; font-weight: normal"> {8} </h3>
       <hr>
       <h2 style ="color:black; text-align: left"> Speaking Times: </h2>
       <h3 style ="color:black; text-align: left; font-weight: normal; padding-left: 40px;"> {4}</h3>
    

    </html>
    """.format(meeting_id, meetingdate, meetingtime, stringnames,
               generalremark, remarkcolor, sentiment, positive, negative)

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    print("sent")

    report_text = """\
    <!DOCTYPE html>
    <html lang="en">
    <link href='//fonts.googleapis.com/css?family=Montserrat:thin,extra-light,light,100,200,300,400,500,600,700,800' 
     rel='stylesheet' type='text/css'>
    <style>    
    
    #roundedbigbox {{
        border-radius: 25px;
        background: white;
        padding: 30px;
        width: 750px;
        height: auto;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.5), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        text-align: center;
        margin: auto;
        position: absolute;
        top: 50%;
        left: 50%;
        margin-top: auto;
        margin-bottom: auto;
        -ms-transform: translate(-50%, -50%);
        transform: translate(-50%, -50%);
        padding-top: 20px;
        padding-bottom: 20px;
        padding-left: 40px;
        padding-right: 40px;
    
    }}
    h1{{
        font-family: 'Helvetica';
        font-size: 40px;
    }}
    
    h2{{
        font-family: 'Helvetica';
        font-size: 20px;
    }}
    
    h3{{
        font-family: 'Helvetica';
        font-size: 20px;
    }}
    
    h4{{
        font-family: 'Helvetica';
        font-size: 16px;
    }}
    </style>
    
    <head>
        <meta charset="UTF-8">
        <title>OKZoomer</title>
    </head>
    <body id=roundedbigbox style="padding-top: 20px">
       <h1 style="text-align: center">Your Meeting Summary</h1>
       <hr>
       <h2 style ="text-align: left;">For meeting <span style="color:#A53FD2; font-weight: normal">{0}</span> on
       <span style="color:#A53FD2; font-weight: normal">{1}</span> at <span style="color:#A53FD2;font-weight: normal">
             {2}</span> </h2>
       <h2 style="text-align: left;"> Attendees: <span style="color:black; font-weight: normal">
          {3} </span></h2>
       <hr>
       <h2 style ="color:black; text-align: left"> {6} </h2> 
       <h4 style ="color:#17B50E; text-align: left; padding-left: 40px; font-weight: normal"> {7} </h4>
       <h4 style ="color:#E37100; text-align: left; padding-left: 40px; font-weight: normal"> {8} </h4>
       <hr>
       <h2 style ="color:black; text-align: left"> Speaking Times: </h2>
       <div>
       <h4 style="float: left;">
       <img src="{{{{url_for('static', filename="{new_graph}")}}}}" width="60%"></h4>
       <h4 style ="color:black; text-align: left; font-weight: normal">
             {4}</h4>
       </div>
    </body>
    </html>
    
    """.format(meeting_id, meetingdate, meetingtime, stringnames,
               generalremark, remarkcolor, sentiment, positive, negative, new_graph=new_graph_name)
    report_file = open("templates/report.html", "w")
    report_file.write(report_text)

    return

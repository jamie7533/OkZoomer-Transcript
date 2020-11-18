import webvtt
from datetime import datetime
from monkeylearn import MonkeyLearn


# Cycles through .vtt file using WebVtt and adds up seconds spoken
# per person in the meeting

def getName(text):
    index = text.find(':')
    nextIndex = text.find(':',index+1)
    if nextIndex != -1:
        index = nextIndex
    if index == -1:
        return "NO NAME FOUND"
    return text[0:index]

def getText(text):
    index = text.find(':')
    nextIndex = text.find(':',index+1)
    if nextIndex != -1:
        index = nextIndex
    if index == -1:
        return text
    return text[index+1:]

def searchName(name, array):
    if array == []:
        return False
    for i in array:
        if i[0]==name:
            return True
    return False

def findName(name, array):
    for index, value in enumerate(array):
        if value[0]==name:
            return index

def timeDiff(time1, time2):
    time1 = datetime.strptime(time1, "%H:%M:%S.%f")
    time2 = datetime.strptime(time2, "%H:%M:%S.%f")
    return tdtoSeconds(time2-time1)

def toSeconds(time):
    time = datetime.strptime(time, "%H:%M:%S.%f")
    return time.second + 60*time.minute + 60*60*time.hour

def tdtoSeconds(time):
    return time.seconds + time.microseconds*.00001

def roundit(array):
    for index, value in enumerate(array):
        array[index][1] = round(value[1])
    return array

def getSentiment(breakdowns):
    for index, value in enumerate(breakdowns):
        breakdowns[index][2] = getVibe([value[2]])
    return breakdowns

def getVibe(data: list):
    ml = MonkeyLearn('e91f245f8c4d03166c8d110036df89f9fa58d055')
    model_id = 'cl_pi3C7JiL'
    result = ml.classifiers.classify(model_id, data)
    vibe = result.body[0].get('classifications')[0].get('tag_name')
    confidence = result.body[0].get('classifications')[0].get('confidence')
    if confidence>=0.8:
        return vibe
    else:
        return 'Neutral'

# This is the big function that cycles thorugh the vtt file
def getBreakdown(vtt):
    breakdowns = []
    for caption in webvtt.read(vtt):
        name = getName(caption.text)
        if name == "NO NAME FOUND":
            pass
        elif searchName(name,breakdowns):
            index = findName(name, breakdowns)
            breakdowns[index][1] = breakdowns[index][1] + timeDiff(caption.start, caption.end)
            breakdowns[index][2] = breakdowns[index][2] + " " + getText(caption.text)
        else:
            breakdowns.append([name,timeDiff(caption.start, caption.end), getText(caption.text)])
    breakdowns = roundit(breakdowns)
    breakdowns = getSentiment(breakdowns)
    for i in breakdowns:
        print(i[0]," talked for ", i[1], " seconds")
        print("Sentiment: ")
        print(i[2])

        #print(caption.start)  # start timestamp in text format
        #print(caption.end)  # end timestamp in text format
        #print(caption.text) # caption texk
    return breakdowns

#getBreakdown("Example Transcript.vtt")
# getBreakdown("94923151321_audio_transcript_first-try.vtt")
# getBreakdown("94923151321_audio_transcript.vtt")
import webvtt
from datetime import datetime

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

# This is the big function that cycles thorugh the vtt file

def getBreakdown(vtt):
    breakdowns = []
    for caption in webvtt.read(vtt):
        name = getName(caption.text)
        if name == "NO NAME FOUND":
            l=1
        elif searchName(name,breakdowns):
            index = findName(name, breakdowns)
            breakdowns[index][1] = breakdowns[index][1] + timeDiff(caption.start, caption.end)
        else:
            breakdowns.append([name,timeDiff(caption.start, caption.end)])
    breakdowns =roundit(breakdowns)
    for i in breakdowns:
        print(i[0]," talked for ", i[1], " seconds")
        #print(caption.start)  # start timestamp in text format
        #print(caption.end)  # end timestamp in text format
        #print(caption.text) # caption text

print(getBreakdown("Example Transcript.vtt"))
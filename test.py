from flask import *
import re
import numpy as np
from array import *
import json
import itertools
import csv
import json
from tika import parser
import textract
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
from datetime import datetime


def getSection(line, code, day, time):

    list = line.split(" ")

    start = 0
    end = 0

    for index, sWord in enumerate(list):

        if(sWord == "R" or sWord == "RSV" or sWord == "R_" ):

            start = index

            s_result = list[start-1]

            return s_result

  


def filter(line, code, day, time):

    list = line.split(" ")

    if(len(list) > 4):

        start = 0
        end = 0

        for index, sWord in enumerate(list):

            if(sWord == day):

                end = index

            if(sWord == "R" or sWord == "RSV" or sWord == "R_" ):

                start = index

        result = ' '.join(list[start+1:end-1])

        s_result = list[start-1]
        print(result)

    # print(day)

        return result


def getSubject(line, code, day, time):

    if re.search('\sAM\s', line):

        strList = line.split(" ")

        for index, sWord in enumerate(strList):
            if sWord == "AM" or sWord == "AM\n":

                i = index

                result = ' '.join(strList[0:i-1])

                new_result = filter(result, code, day, time)

    elif re.search('\sPM\s', line):

        strList = line.split(" ")

        for index, sWord in enumerate(strList):
            if sWord == "PM" or sWord == "PM\n":

                i = index

                result = ' '.join(strList[0:i])

                new_result = filter(result, code, day, time)

    return new_result


def process(f):

    pdf = wi(filename=f, resolution=300)
    pdfImage = pdf.convert('jpeg')

    imageBlobs = []

    for img in pdfImage.sequence:
        imgPage = wi(image=img)
        imageBlobs.append(imgPage.make_blob('jpeg'))

    recognized_text = []

    for imgBlob in imageBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang='eng')
        recognized_text.append(text)

    file = open('a.txt', 'w')

    file.write(text)

    file.close()

    print("done")

    with open("a.txt", "r") as ins:
        array = []
        for line in ins:
            array.append(line)

    # print(array)

    # array.append(text)'''

    line = []
    line_code = []
    line_time = []
    line_day = []

    monformat = []
    tueformat = []
    wedformat = []
    thurformat = []
    friformat = []

    mon = []
    tue = []
    wed = []
    thur = []
    fri = []

    montime = []
    tuetime = []
    wedtime = []
    thurtime = []
    fritime = []

    i = 0

    prevline = ""

    #RAPATKAN MASA

    while i < len(array):

        if re.search("MON", array[i]):

            line.append(array[i])
            line_day.append("MON")

            if re.findall("\w{2,4}\s\d{4}", array[i]):

                code = re.findall("\w{2,4}\s\d{4}", array[i])

                mon.append(code)
                line_code.append(code)

            elif re.findall("\w{2,4}\s\d{4}", prevline):

                code1 = re.findall("\w{2,4}\s\d{4}", prevline)

                mon.append(code1)
                line_code.append(code1)

            elif re.findall("\w{2,4}\s\d{4}", array[i-2]):

                code2 = re.findall("\w{2,4}\s\d{4}", array[i-2])

                mon.append(code2)
                line_code.append(code2)

            else:

                code3 = re.findall("\w{2,4}\s\d{4}", array[i-3])

                mon.append(code3)
                line_code.append(code3)

            # for time

            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i])

                montime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                montime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i])

                montime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i])

                montime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                montime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                montime.append(date)
                line_time.append(date)

            # for format

            if re.search('\sAM\s', array[i]):

                monformat.append("AM")

            elif re.search('\sPM\s', array[i]):

                monformat.append("PM")

        elif re.search("M-W", array[i]):

            line.append(array[i])
            line_day.append("M-W")

            if re.findall("\w{2,4}\s\d{4}", array[i]):

                code = re.findall("\w{2,4}\s\d{4}", array[i])

                mon.append(code)
                wed.append(code)
                line_code.append(code)

            elif re.findall("\w{2,4}\s\d{4}", prevline):

                code1 = re.findall("\w{2,4}\s\d{4}", prevline)

                mon.append(code1)
                wed.append(code1)
                line_code.append(code1)

            else:

                code2 = re.findall("\w{2,4}\s\d{4}", array[i-2])

                mon.append(code2)
                wed.append(code2)
                line_code.append(code2)

            # for time

            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i])

                montime.append(date)
                wedtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                montime.append(date)
                wedtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i])

                montime.append(date)
                wedtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i])

                montime.append(date)
                wedtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                montime.append(date)
                wedtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                montime.append(date)
                wedtime.append(date)
                line_time.append(date)
            # for format

            if re.search('\sAM\s', array[i]):

                monformat.append("AM")
                wedformat.append("AM")

            elif re.search('\sPM\s', array[i]):

                monformat.append("PM")
                wedformat.append("PM")

        elif re.search("TUE", array[i]):

            line.append(array[i])
            line_day.append("TUE")

            if re.findall("\w{2,4}\s\d{4}", array[i]):

                code = re.findall("\w{2,4}\s\d{4}", array[i])

                tue.append(code)
                line_code.append(code)

            elif re.findall("\w{2,4}\s\d{4}", prevline):

                code1 = re.findall("\w{2,4}\s\d{4}", prevline)

                tue.append(code1)
                line_code.append(code1)

            else:

                code2 = re.findall("\w{2,4}\s\d{4}", array[i-2])

                tue.append(code2)
                line_code.append(code2)

            # for time

            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i])

                tuetime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                tuetime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i])

                tuetime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i])

                tuetime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\s\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s\s[\\-]\s\d{1,2}\.\d{2}", array[i])

                tuetime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                tuetime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                tuetime.append(date)
                line_time.append(date)
            # for format

            if re.search('\sAM\s', array[i]):

                tueformat.append("AM")

            elif re.search('\sPM\s', array[i]):

                tueformat.append("PM")

        elif re.search("THU", array[i]):

            line.append(array[i])
            line_day.append("THU")

            if re.findall("\w{2,4}\s\d{4}", array[i]):

                code = re.findall("\w{2,4}\s\d{4}", array[i])

                thur.append(code)
                line_code.append(code)

            elif re.findall("\w{2,4}\s\d{4}", prevline):

                code1 = re.findall("\w{2,4}\s\d{4}", prevline)

                thur.append(code1)
                line_code.append(code1)

            else:

                code2 = re.findall("\w{2,4}\s\d{4}", array[i-2])

                thur.append(code2)
                line_code.append(code2)

            # for time

            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i])

                thurtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                thurtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i])

                thurtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i])

                thurtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                thurtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                thurtime.append(date)
                line_time.append(date)

            # for format

            if re.search('\sAM\s', array[i]):

                thurformat.append("AM")

            elif re.search('\sPM\s', array[i]):

                thurformat.append("PM")

        elif re.search("T-TH", array[i]):

            line.append(array[i])
            line_day.append("T-TH")

            if re.findall("\w{2,4}\s\d{4}", array[i]):
                code = re.findall("\w{2,4}\s\d{4}", array[i])

                tue.append(code)
                thur.append(code)
                line_code.append(code)

            elif re.findall("\w{2,4}\s\d{4}", prevline):

                code1 = re.findall("\w{2,4}\s\d{4}", prevline)

                tue.append(code1)
                thur.append(code1)
                line_code.append(code1)

            else:

                code2 = re.findall("\w{2,4}\s\d{4}", array[i-2])

                tue.append(code2)
                thur.append(code2)
                line_code.append(code2)

            # for time

            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i])

                tuetime.append(date)
                thurtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                tuetime.append(date)
                thurtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i])

                tuetime.append(date)
                thurtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i])

                tuetime.append(date)
                thurtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                tuetime.append(date)
                thurtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                tuetime.append(date)
                thurtime.append(date)
                line_time.append(date)

            # for format

            if re.search('\sAM\s', array[i]):

                tueformat.append("AM")
                thurformat.append("AM")

            elif re.search('\sPM\s', array[i]):

                tueformat.append("PM")
                thurformat.append("PM")

        elif re.search("WED", array[i]):

            line.append(array[i])
            line_day.append("WED")

            if re.findall("\w{2,4}\s\d{4}", array[i]):
                code = re.findall("\w{2,4}\s\d{4}", array[i])

                wed.append(code)
                line_code.append(code)

            elif re.findall("\w{2,4}\s\d{4}", prevline):

                code1 = re.findall("\w{2,4}\s\d{4}", prevline)

                wed.append(code1)
                line_code.append(code1)

            elif re.findall("\w{2,4}\s\d{4}", array[i-2]):

                code1 = re.findall("\w{2,4}\s\d{4}", array[i-2])

                wed.append(code1)
                line_code.append(code1)

            else:

                code2 = re.findall("\w{2,4}\s\d{4}", array[i-3])

                wed.append(code2)
                line_code.append(code2)

            # for time

            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i])

                wedtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                wedtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i])

                wedtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i])

                wedtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                wedtime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                wedtime.append(date)
                line_time.append(date)

            # for format

            if re.search('\sAM\s', array[i]):

                wedformat.append("AM")

            elif re.search('\sPM\s', array[i]):

                wedformat.append("PM")

        elif re.search("FRI", array[i]):

            line.append(array[i])
            line_day.append("FRI")

            if re.findall("\w{2,4}\s\d{4}", array[i]):

                code = re.findall("\w{2,4}\s\d{4}", array[i])

                fri.append(code)
                line_code.append(code)

            elif re.findall("\w{2,4}\s\d{4}", prevline):

                code1 = re.findall("\w{2,4}\s\d{4}", prevline)

                fri.append(code1)
                line_code.append(code1)

            elif re.findall("\w{2,4}\s\d{4}", array[i-2]):

                code1 = re.findall("\w{2,4}\s\d{4}", array[i-2])

                fri.append(code1)
                line_code.append(code1)

            else:

                code2 = re.findall("\w{2,4}\s\d{4}", array[i-3])

                fri.append(code2)
                line_code.append(code2)

            # for time

            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}", array[i])

                fritime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                fritime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}", array[i])

                fritime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}", array[i])

                fritime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall(
                    "\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                fritime.append(date)
                line_time.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i]):

                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}", array[i])

                fritime.append(date)
                line_time.append(date)

            # for format

            if re.search('\sAM\s', array[i]):

                friformat.append("AM")

            elif re.search('\sPM\s', array[i]):

                friformat.append("PM")

        else:

            None

        prevline = array[i]
        i += 1

    # for x in line:
    #     getSubject(x,)

    name = []
    name_code = []
    section_code = []
    event = []

    for i in line_time:
        print(i)

    

    for x, y in enumerate(line):
        getName = getSubject(line[x], line_code[x], line_day[x], line_time[x])
        section = getSection(line[x], line_code[x], line_day[x], line_time[x])
        name.append(getName)
        name_code.append(line_code[x])
        section_code.append(section)
        name_event = "event-"+str(x+1) 
        event.append(name_event)

    # remove bracket for every list
    course_code = []
    course_code = [i[0] for i in name_code]

    # remove none value in the array

    for x, y in enumerate(name):
        if(name[x] == None):
            name.pop(x)
            course_code.pop(x)
            section_code.pop(x)
            event.pop(x)

    # for x, y in enumerate(name):
    #     print(event[x],"- ",name[x],"-",course_code[x])

    lengthmon = len(mon)
    lengthtue = len(tue)
    lengthwed = len(wed)
    lengththur = len(thur)
    lengthfri = len(fri)

    daymon = []
    daytue = []
    daywed = []
    daythur = []
    dayfri = []

    i = 0

    while i < len(mon):
        daymon.insert(i, "MON")

        i += 1

    i = 0
    while i < len(tue):
        daytue.insert(i, 'TUE')

        i += 1

    i = 0
    while i < len(wed):
        daywed.insert(i, 'WED')

        i += 1

    i = 0
    while i < len(thur):
        daythur.insert(i, 'THUR')

        i += 1

    i = 0
    while i < len(fri):
        dayfri.insert(i, 'FRI')

        i += 1

    day = []
    start_time = []

    mon = [i[0] for i in mon]
    montime = [i[0] for i in montime]
    tue = [i[0] for i in tue]
    tuetime = [i[0] for i in tuetime]
    wed = [i[0] for i in wed]
    wedtime = [i[0] for i in wedtime]
    thur = [i[0] for i in thur]
    thurtime = [i[0] for i in thurtime]
    fri = [i[0] for i in fri]
    fritime = [i[0] for i in fritime]

    start_time_temp= [i.split('-')[0] for i in montime]
    end_time_temp = [i.split('-')[1] for i in montime]

    start_time_tue_temp = [i.split('-')[0] for i in tuetime]
    end_time_tue_temp = [i.split('-')[1] for i in tuetime]

    start_time_wed_temp = [i.split('-')[0] for i in wedtime]
    end_time_wed_temp = [i.split('-')[1] for i in wedtime]

    start_time_thur_temp = [i.split('-')[0] for i in thurtime]
    end_time_thur_temp = [i.split('-')[1] for i in thurtime]

    start_time_fri_temp = [i.split('-')[0] for i in fritime]
    end_time_fri_temp = [i.split('-')[1] for i in fritime]

    start_time = [i.replace('.', ':') for i in start_time_temp]
    end_time = [i.replace('.', ':') for i in end_time_temp]

    start_time_tue =[i.replace('.', ':') for i in start_time_tue_temp]
    end_time_tue =[i.replace('.', ':') for i in end_time_tue_temp]

    start_time_wed = [i.replace('.', ':') for i in start_time_wed_temp ]
    end_time_wed =[i.replace('.', ':') for i in end_time_wed_temp]

    start_time_thur = [i.replace('.', ':') for i in start_time_thur_temp]
    end_time_thur = [i.replace('.', ':') for i in  end_time_thur_temp]

    start_time_fri =[i.replace('.', ':') for i in start_time_fri_temp]
    end_time_fri =[i.replace('.', ':') for i in end_time_fri_temp]



  

    mon_name = []
    tue_name = []
    wed_name = []
    thur_name = []
    fri_name = []

    mon_section = []
    tue_section = []
    wed_section = []
    thur_section = []
    fri_section = []

    mon_event = []
    tue_event = []
    wed_event = []
    thur_event = []
    fri_event = []

    # insert course name

    for course in mon:
        for x, code in enumerate(course_code):
            if(course == code):
                mon_name.append(name[x])
                mon_section.append(section_code[x])
                mon_event.append(event[x])

    for course in tue:
        for x, code in enumerate(course_code):
            if(course == code):
                tue_name.append(name[x])
                tue_section.append(section_code[x])
                tue_event.append(event[x])

    for course in wed:
        for x, code in enumerate(course_code):
            if(course == code):
                wed_name.append(name[x])
                wed_section.append(section_code[x])
                wed_event.append(event[x])

    for course in thur:
        for x, code in enumerate(course_code):
            if(course == code):
                thur_name.append(name[x])
                thur_section.append(section_code[x])
                thur_event.append(event[x])

    for course in fri:
        for x, code in enumerate(course_code):
            if(course == code):
                fri_name.append(name[x])
                fri_section.append(section_code[x])
                fri_event.append(event[x])

    #OTHER WAY TO COMBINE ALL DATA
    # day1 = tuple(zip(daymon, mon, mon_name, mon_section,
    #              start_time, end_time, monformat))
    # day2 = tuple(zip(daytue, tue, tue_name, tue_section,
    #              start_time_tue, end_time_tue, tueformat))
    # day3 = tuple(zip(daywed, wed, wed_name, wed_section,
    #              start_time_wed, end_time_wed, wedformat))
    # day4 = tuple(zip(daythur, thur, thur_name, thur_section,
    #              start_time_thur, end_time_thur, thurformat))
    # day5 = tuple(zip(dayfri, fri, fri_name, fri_section,
    #              start_time_fri, end_time_fri, friformat))

    # document = day1+day2+day3+day4+day5

    #ASSIGN EVENT FOR EACH SUBJECT

    z = mon + tue + wed + thur + fri

    
    event = [z[i] for i in range(len(z)) if i == z.index(z[i])]
    # print(z)
    # print(event)

    data = {}
    data['monday'] = []  
    data['tuesday'] = []  
    data['wednesday'] = []  
    data['thursday'] = []  
    data['friday'] = []  

    #JSON SECTION MONDAY
    for index in range(len(mon)):
        
        data['monday'].append({
            'code': mon[index],
            'name': mon_name[index],
            'section':mon_section[index],
            'start_time': start_time[index],
            'end_time': end_time[index],
            'time_format': monformat[index] ,
            'event':mon_event[index]
        })      

    #JSON SECTION TUESDAY
    for index in range(len(tue)):
        
        data['tuesday'].append({
            'code': tue[index],
            'name': tue_name[index],
            'section':tue_section[index],
            'start_time': start_time_tue[index],
            'end_time': end_time_tue[index],
            'time_format': tueformat[index],
            'event':tue_event[index]
        })    


    #JSON SECTION WEDENESDAY
    for index in range(len(wed)):
        
        data['wednesday'].append({
            'code': wed[index],
            'name': wed_name[index],
            'section':wed_section[index],
            'start_time': start_time_wed[index],
            'end_time': end_time_wed[index],
            'time_format': wedformat[index],
            'event':wed_event[index]
        })     

    #JSON SECTION THURSDAY
    for index in range(len(thur)):
        
        data['thursday'].append({
            'code': thur[index],
            'name': thur_name[index],
            'section':thur_section[index],
            'start_time': start_time_thur[index],
            'end_time': end_time_thur[index],
            'time_format': thurformat[index],
            'event':thur_event[index] 
        })  

    #JSON SECTION FRIDAY
    for index in range(len(fri)):
        
        data['friday'].append({
            'code': fri[index],
            'name': fri_name[index],
            'section':fri_section[index],
            'start_time': start_time_fri[index],
            'end_time': end_time_fri[index],
            'time_format': friformat[index],
            'event':fri_event[index]
        })     

    
    #TURN THE DATA INTO CSV FORMAT AND TO CSV FILE
    # header = ['DAY', 'SUBJECT', 'NAME', 'SECTION', 'START', 'END', 'FORMAT']

    # with open('timetable.csv', 'w', newline='') as csvFile:
    #     writer = csv.writer(csvFile)
    #     writer.writerow(header)

    # with open('timetable.csv', 'a', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(document)

    # csvFilePath = "timetable.csv"
    # jsonFilePath = "timetable.json"
    # arr = []
    # # read the csv and add the arr to a arrayn

    # with open(csvFilePath) as csvFile:
    #     csvReader = csv.DictReader(csvFile)
    #     # print(csvReader)
    #     for csvRow in csvReader:
    #         arr.append(csvRow)

    '''with open(jsonFilePath, "w") as jsonFile:
        jsonFile.write(json.dumps(arr, indent = 5))'''

    # data = json.dumps(arr, indent=5)

    print(data)
    return data


process("C:\\Users\\Lenovo 110\\Desktop\\database-schedule\\helloworld\\Confirmation Slip latest.pdf")

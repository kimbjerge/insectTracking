# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 08:25:25 2020

@author: Kim Bjerge
         Aarhus University
"""

import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Label names for plot

#labelNames = ["Mariehone", "Honningbi", "Stenhumle", "Jordhumle", "Svirrehvid", "Svirregul", "Flue", "Sommerfugl"] # Danish names
labelNames = ["Conccinellidae sept.", "Apis mellifera", "Bombus lapidarius", "Bombus terrestris", "Eupeodes corolla", "Episyrphus balteatus", "Unknown", "Aglais urticae"]

# Functions to get seconds, minutes and hours from time in predictions
def getSeconds(recTime):
    return int(recTime%100)

def getMinutes(recTime):
    minSec = recTime%10000
    return int(minSec/100)

def getHours(recTime):
    return int(recTime/10000)

# Functions to get day, month and year from date in predictions
def getDay(recDate):
    return int(recDate%100)

def getMonthDay(recDate):
    return int(recDate%10000)

def getMonth(recDate):
    return int(getMonthDay(recDate)/100)

def getYear(recDate):
    return int(recDate/10000)

def convertToJson(line):
    
    line = line.replace("'", '"')
    
    lineList = list(line)
    idx = line.find("starttime")
    starttime = line[idx+12:idx+20]
    for i in range(8):
        lineList[idx+12+i] = ' '
    lineList[idx+19] = '1'    
    #print(starttime)
    idx = line.find("endtime")
    endtime = line[idx+10:idx+18]
    for i in range(8):
        lineList[idx+10+i] = ' ' 
    lineList[idx+17] = '1'    
    #print(endtime)
    
    newLine = "".join(lineList)
    newLine = newLine[0:-2]
    return newLine, starttime, endtime

# Load tracks JSON file
def load_tracks_json(filename, selection = 'All'):
    
    foundObjects = []
    track_file = open(filename, 'r')
    
    for l in track_file:
        line, starttime, endtime = convertToJson(l)
        track = json.loads(line)
        classId = -1
        for j in range(len(labelNames)):
            if track['class'] == labelNames[j]:
                classId = j              
        record = {'id': track['id'],
                'startdate':  track['startdate'], 
                'starttime' :  starttime,
                'endtime' :  endtime,
                'duration' :  track['duration'], 
                'className' :  track['class'],
                'class' : classId+1,
                'counts' :  track['counts'],
                'confidence' :  track['confidence'],
                'size' :  track['size'],
                'distance' :  track['distance']} # Class label (Unknown = 0)                
        if  classId > -1: 
            foundObjects.append(record)
            #print(record)

    track_file.close()  
          
    return foundObjects


# Plots number of bees and svirrefluer as function of dates where insects found
def plotInsectsDate(json_file):
    
    tracks = load_tracks_json(json_file, selection = 'All') 
    
    currDate = 0
    monthArray = []
    marie = []
    bees = []
    humle = []
    svirre = []
    dayArray = []
    idx = -1
    for track in tracks:
        if currDate != track['startdate']:
            currDate = track['startdate']
            monthArray.append(getMonthDay(currDate))
            marie.append(0)
            bees.append(0)
            humle.append(0)
            svirre.append(0)
            idx += 1
            dayArray.append(idx)
        classObj = track['class']
        if classObj == 1: #mariehøne (1)
            marie[idx] += 1
        if classObj == 2: #honnigbi (2)
            bees[idx] += 1
        if classObj >= 3 and classObj <= 4: #stenhumle (3), jordhumle (4)
            humle[idx] += 1
        if classObj >= 5 and classObj <= 6: #svirrehvid (5), svirregul (6)
            svirre[idx] += 1
  
    fig = plt.figure(figsize=(17,15))
    ax = fig.add_subplot(2, 1, 1, axisbg="1.0")         
    ax.plot(dayArray, marie, 'ro', label='Mariehøne')
    ax.plot(dayArray, bees, 'go', label='Honningbi')
    ax.plot(dayArray, humle, 'bo', label='Humlebi')
    ax.plot(dayArray, svirre, 'yo', label='Svirreflue')
    ax.legend(loc=2)
    ax.set_ylim(0, 50)
    ax.set_xlabel('Dage')
    ax.set_ylabel('Antal')
    ax.set_title('Insekter fra ' + str(currDate))
    ax.grid(True)
    fig.tight_layout()
    plt.show()

    #print("Dates:", monthArray) 

# Create an array with month and day for whole periode
def convertPeriode(periode):
    
    monthDayArray = []
    for date in periode:
        currDate = int(date)
        monthDayArray.append(currDate)
            
    return monthDayArray

# Create an array with month and day for whole periode
def createPeriode(periode):
    
    monthDayArray = []
    currDate = periode[0]
    while currDate <= periode[1]+1:
        monthDayArray.append(currDate)
        currDate += 1
        month = getMonth(currDate)
        if getDay(currDate) == 31 and (month == 6 or month == 9): # June and September 30 days
            currDate += (100-30);
        if getDay(currDate) == 32 and (month == 5 or month == 7 or month == 8): # May, July and August 31 days
            currDate += (100-31);
            
    return monthDayArray

# Get index that belongs to date
def getDateIdx(currMonthDay, monthDayArray):
    
    for idx in range(len(monthDayArray)):
        if currMonthDay == monthDayArray[idx]:
            return idx

    return 0

# Fundtion to create format of x-axis
globalMonthDayArray = createPeriode([625, 1005])

@ticker.FuncFormatter
def major_formatter(x, pos):
    day = int(globalMonthDayArray[int(x)] % 100)
    month = int(globalMonthDayArray[int(x)] / 100)
    string =  "{}/{}-2019"
    return string.format(day, month) #"%d" % day

# Plots number of bees and svirrefluer as function of periode with all dates
def plotInsectsPeriode(path, periode):
    
    allTracks = []
    for date in periode:
        json_file = path + "2020" + date + '.json'
        tracks = load_tracks_json(json_file, selection = 'All') 
        allTracks = allTracks + tracks

    totalTracks = 0
    totalImages = 0
    classCounts = []
    avgSize = 0
    lenght = len(labelNames)
    for i in range(lenght):
        classCounts.append(0)

    #currDate = 0
    monthArray = convertPeriode(periode)
    length = len(monthArray)
    marie = np.zeros((length,), dtype=int)
    bees = np.zeros((length,), dtype=int)
    humle = np.zeros((length,), dtype=int)
    svirre = np.zeros((length,), dtype=int)
    sommer = np.zeros((length,), dtype=int)
    totalInsects = np.zeros((length,), dtype=int)
    dayArray = range(length)
    idx = -1
    for track in allTracks:
        idx = getDateIdx(getMonthDay(track['startdate']), monthArray)
        classObj = track['class']
        classCounts[classObj-1] += 1
        totalTracks += 1
        totalImages += track['counts']
        avgSize += track['size']
        totalInsects[idx] += 1
        if classObj == 1: #mariehøne (1)
            marie[idx] += 1
        if classObj == 2: #honnigbi (2)
            bees[idx] += 1
        if classObj >= 3 and classObj <= 4: #stenhumle (3), jordhumle (4)
            humle[idx] += 1
        if classObj >= 5 and classObj <= 6: #svirrehvid (5), svirregul (6)
            svirre[idx] += 1
        if classObj == 8: 
            sommer[idx] += 1
  
    print(classCounts, totalTracks, totalImages, avgSize/totalTracks)
    print(totalInsects)
    print(bees)
    
    matplotlib.rcParams.update({'font.size': 22})
    fig = plt.figure(figsize=(30,30))
    ax = fig.add_subplot(2, 1, 1, axisbg="1.0")         
    ax.plot(dayArray, marie, 'r', label='Ladybugs') #Mariehøns
    ax.plot(dayArray, bees, 'g', label='Honeybees') #Honning bier
    ax.plot(dayArray, humle, 'b', label='Bumblebees') #Hummel bier
    ax.plot(dayArray, svirre, 'y', label='Hoverflies') #Svirrefluer
    ax.plot(dayArray, sommer, 'm', label='Butterfies') #Sommerfugle
    ax.legend(loc=2)
    ax.xaxis.set_major_formatter(major_formatter)
    #ax.set_yscale('log')
    ax.set_ylim(0, 100)
    #ax.set_ylim(0, 240)
    ax.set_xlabel('Date')
    ax.set_ylabel('Counts')
    ax.set_title('Observed insect tracks')
    ax.grid(True)
    fig.tight_layout()
    plt.show()
    fig.savefig('../results/insectsPeriode.jpg')   
    plt.close(fig)   
    matplotlib.rcParams.update({'font.size': 12})
    
    return [dayArray, monthArray, marie, bees, humle, svirre, sommer]
     
def plotHistogramPeriode(path, periode, ClassIds):
    
    allTracks = []
    for date in periode:
        json_file = path + "2020" + date + '.json'
        tracks = load_tracks_json(json_file, selection = 'All') 
        allTracks = allTracks + tracks
    
    dur = []
    meanDur = 0
    cntDur = 0
    for track in allTracks:
        #idx = getDateIdx(getMonthDay(track['startdate']), monthArray)
        for Id in ClassIds:
            if track['class'] == Id: 
                if track['duration'] < 500: # Remove out liers
                    #dur.append(track['distance'])
                    dur.append(track['duration'])
                    if track['class'] == 2: # Honey bee
                       #meanDur += track['distance']
                       meanDur += track['duration']
                       cntDur += 1

    matplotlib.rcParams.update({'font.size': 20})
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1, 1, 1, axisbg="1.0")    
    ax.hist(dur, density=True, bins=100)  # `density=False` would make counts
    ax.set_ylabel('Density')
    ax.set_xlabel('Duration (seconds)')
    #ax.set_xlabel('Distance (pixels)')
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 0.08)
    #ax.set_xlim(0, 180)
    #ax.set_ylim(0, 0.08)
    #className = labelNames[Id-1]

    titleName = ""
    if Id == 1:
        titleName = 'Ladybugs'
    if Id == 2:
        titleName = 'Honeybees'
    if Id == 3 or Id == 4:
        titleName = 'Bumblebees'
    if Id == 5 or Id == 6:
        titleName = 'Hoverflies'
    if Id == 8:
        titleName = 'Butterfies'
        
    ax.set_title(titleName)
    plt.savefig("../results/" + titleName+'.jpg')
    plt.show()
    matplotlib.rcParams.update({'font.size': 12})
    
    if cntDur > 0:
        print("Average duration for Honeybees:", meanDur/cntDur)
    

if __name__=='__main__': 
    
    path = '../tracks/'
    
    #json_name = path + "20200625.json"
    #plotInsectsDate(json_name)

    periode = ["0625",
               "0626", 
               "0627", 
               "0628", 
               "0629", 
               "0630", 
               "0701", 
               "0702", 
               "0703", 
               #"0704", 
               #"0705", 
               "0706", 
               "0707", 
               "0708", 
               "0709", 
               "0710", 
               "0711", 
               "0712", 
               "0713", 
               "0714", 
               "0715", 
               "0716", 
               "0717", 
               "0718", 
               "0719", 
               "0720", 
               "0721", 
               "0722", 
               "0723", 
               "0724", 
               "0725", 
               "0726", 
               "0727", 
               "0728", 
               "0729", 
               "0730", 
               "0731", 
               #"0801", 
               #"0802", 
               "0803", 
               "0804", 
               "0805", 
               "0806", 
               "0807", 
               "0808", 
               "0810",                
               "0811", 
               "0812", 
               "0813",  
               "0814",  
               "0815",
               "0816",
               "0817",               
               "0818",
               "0819",
               "0820",
               "0821",               
               "0822",               
               "0823",
               "0824",
               "0825",
               "0826",
               "0827",
               "0828",
               "0829",
               "0830",
               #"0831",
               "0901",
               "0902",
               "0903",
               "0904",
               "0905",
               "0906",
               "0907",
               "0908",
               "0909",
               "0910",
               "0911",
               "0912",
               "0913",
               "0914",
               "0915",
               "0916",
               "0917",
               "0918",
               "0919",
               "0920",
               "0921",
               "0922",
               "0923",
               "0924",
               "0925",
               "0926",
               "0927",
               "0928",
               "0929"
               ]
    
    #periode = [ "0811", "0812", "0813",  "0814",  "0815", "0816", "0817", "0822" ]
    
    plotInsectsPeriode(path, periode)
    plotHistogramPeriode(path, periode, [1])
    plotHistogramPeriode(path, periode, [2])
    plotHistogramPeriode(path, periode, [3,4])
    plotHistogramPeriode(path, periode, [5,6])
    plotHistogramPeriode(path, periode, [8])

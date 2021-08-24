# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 12:48:13 2020

@author: Kim Bjerge
"""

import math
from idac.objectOfInterrest import ObjectOfInterrest

class Predictions:
    
    def __init__(self, conf):
        print('predictions')
        self.config = conf["classifier"]
        self.species = self.config["species"]
        self.noPredicions = 0
        self.noFilteredPredicions = 0


    def getPredictions(self):
        return self.noPredicions, self.noFilteredPredicions
        
    # Functions to get seconds, minutes and hours from time in predictions
    def getSeconds(self, recTime):
        return int(recTime%100)
    
    def getMinutes(self, recTime):
        minSec = recTime%10000
        return int(minSec/100)
    
    def getHours(self, recTime):
        return int(recTime/10000)
    
    def getTimesec(self, recTime):
        
        timestamp = self.getSeconds(recTime)
        timestamp += self.getMinutes(recTime)*60
        timestamp += self.getHours(recTime)*3600
        return timestamp
    
    # Functions to get day, month and year from date in predictions
    def getDay(self, recDate):
        return int(recDate%100)
    
    def getMonthDay(self, recDate):
        return int(recDate%10000)
    
    def getMonth(self, recDate):
        return int(self.getMonthDay(recDate)/100)
    
    def getYear(self, recDate):
        return int(recDate/10000)
        
    # Substract filterTime in minutes from recTime, do not handle 00:00:00
    def substractMinutes(self, recTime, filterTime):
        
        minute = self.getMinutes(recTime)
        
        newRecTime = recTime - int(filterTime)*100
        if minute < filterTime: # No space to substract filterTime
            newRecTime = newRecTime - 4000 # Adjust minutes
        
        return newRecTime
    
    # Filter predictions - if the positions are very close and of same class
    # Checked within filterTime in minutes (must be a natural number 0,1,2..60)
    # It is is assumed that the new prediction belong to the same object
    def filter_prediction(self, lastPredictions, newPrediction, filterTime):
        
        newObject = True
        
        # Filter disabled
        if filterTime == 0:
            return lastPredictions, newObject
        
        # Update last predictions within filterTime window
        timeWindow = self.substractMinutes(newPrediction['time'], filterTime)
        newLastPredictions = []
        for lastPredict in lastPredictions:
            # Check if newPredition is the same date as last predictions and within time window
            if (lastPredict['date'] == newPrediction['date']) and (lastPredict['time'] > timeWindow):
                newLastPredictions.append(lastPredict)
        
        # Check if new predition is found in last Preditions - nearly same position and class
        for lastPredict in newLastPredictions:
            # Check if new prediction is of same class
            if lastPredict['class'] == newPrediction['class']:
                xlen = lastPredict['xc'] - newPrediction['xc']
                ylen = lastPredict['yc'] - newPrediction['yc']
                # Compute distance between predictions
                dist = math.sqrt(xlen*xlen + ylen*ylen)
                #print(dist)
                if dist < 25: # NB adjusted for no object movement
                    # Distance between center of boxes are very close
                    # Then we assume it is not a new object
                    newObject = False
        
        self.noPredicions += 1
        if newObject == False:
            self.noFilteredPredicions += 1

        # Append new prediction to last preditions
        newLastPredictions.append(newPrediction)
        
        return newLastPredictions, newObject
        
    # Load prediction CSV file
    # filterTime specifies in minutes how long time window used
    # to decide if predictions belongs to the same object
    # probability threshold for each class, default above 50%
    def load_predictions(self, filename, selection = 'All', filterTime=0, threshold=[50,50,50,50,50,50,50,50]):
        
        file = open(filename, 'r')
        content = file.read()
        file.close()
        splitted = content.split('\n')
        lines = len(splitted)
        foundObjects = []
        lastObjects = []
        for line in range(lines):
            subsplit = splitted[line].split(',')
            if len(subsplit) == 11: # required 11 data values
                imgname = subsplit[10]
                imgpath = imgname.split('/')
                prob = int(subsplit[4])
                objClass = int(subsplit[5])
                # Check selection 
                if (selection == imgpath[0] or selection == 'All') and prob >= threshold[objClass-1]:
                    x1 = int(subsplit[6])
                    y1 = int(subsplit[7])
                    x2 = int(subsplit[8])
                    y2 = int(subsplit[9])
                    # Convert points of box to YOLO format: center point and w/h
                    width = x2-x1
                    height = y2-y1
                    xc = x1 - round(width/2)
                    if xc < 0: xc = 0
                    yc = y1 - round(height/2)
                    if yc < 0: yc = 0
                    
                    record = {'system': subsplit[0], # 1-5
                    'camera': int(subsplit[1]), # 0 or 1
                    'date' : int(subsplit[2]),
                    'time' : int(subsplit[3]),
                    'prob' : prob, # Class probability 0-100%
                    'class' : objClass, # Classes 1-8
                    # Box position and size
                    'x1' : x1,
                    'y1' : y1,
                    'x2' : x2,
                    'y2' : y2,
                    'xc' : xc,
                    'yc' : yc,
                    'w' : width,
                    'h' : height,
                    'image' : imgpath[1],
                    'pathimage' : subsplit[10],
                    'label' : 0} # Class label (Unknown = 0)
                    
                    lastObjects, newObject =  self.filter_prediction(lastObjects, record, filterTime)
                    if newObject:
                        foundObjects.append(record)
                
        return foundObjects

    # Find bounding boxes and classes found in image by filename
    def findboxes(self, filename, predictions):
         
        ooi = []
        count = 0
        for predict in predictions:
            if filename == predict['image']:
                obj = ObjectOfInterrest(predict['x1'], predict['y1'], predict['w'], predict['h'])
                obj.label = self.species[predict['class']-1]
                obj.percent = self.getTimesec(predict['prob']) 
                obj.timesec = self.getTimesec(predict['time']) 
                print(obj.label, obj.percent, obj.timesec)
                ooi.append(obj)
                count = count + 1

        return count, ooi
         
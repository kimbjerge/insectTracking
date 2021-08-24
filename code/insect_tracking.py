# -*- coding: utf-8 -*-
"""
Created on Mon May  4 08:10:16 2020

@author: Kim Bjerge
         Aarhus University
"""
#import os
import time
from skimage import io
#from pathlib import Path
from idac.configreader.configreader import readconfig
from idac.datareader.data_reader import DataReader
from idac.tracker.tracker import Tracker
#from idac.blobdet.blob_detector_factory import BlobDetectorFactory
from idac.imagemod.image_mod import Imagemod
from idac.moviemaker.movie_maker import MovieMaker
#from idac.classifier.classifier_factory import ClassifierFactory
from idac.stats.stats import Stats
from idac.predictions.predictions import Predictions
from idac.tracksSave.tracksSave import TracksSave
from PyQt5.QtGui import QImage

# Label names for plot
#labelNames = ["Mariehone", "Honningbi", "Stenhumle", "Jordhumle", "Svirrehvid", "Svirregul", "Flue", "Sommerfugl"] # Danish names
labelNames = ["Conccinellidae sept.", "Apis mellifera", "Bombus lapidarius", "Bombus terrestris", "Eupeodes corolla", "Episyrphus balteatus", "Unknown", "Aglais urticae"]

       
def run(dirName):
    config_filename = '../config/ITC_config.json'
    conf = readconfig(config_filename)
    conf['datareader']['datapath'] += '/' + dirName
    print(conf['datareader']['datapath'])
    #total = len(os.listdir(conf['datareader']['datapath']))
    print(conf['moviemaker']['resultdir'])
    writemovie = conf['moviemaker']['writemovie']
    reader = DataReader(conf)
    gen = reader.getimage()
    print(type(gen))
    #bl = BlobDetectorFactory.get_blob_detector(conf['blobdetector']['type'], conf)
    tr = Tracker(conf)
    imod = Imagemod()
    if dirName == '':
        dirName = 'tracks'
    mm = MovieMaker(conf, name=dirName + '.avi')
    #clas = ClassifierFactory.get_classifier(conf['classifier']['type'], conf)
    stat = Stats(conf)
    predict = Predictions(conf)
    tracksFilename = conf['moviemaker']['resultdir']+'/'+dirName+'TRS.csv'
    print(tracksFilename)
    tracks = TracksSave(tracksFilename)

    csvFilename = '../CSV/'+dirName+'.csv'
    threshold=[10,10,10,10,10,10,10,10]
    predicted = predict.load_predictions(csvFilename, filterTime=5, threshold=threshold) # Skip if not moved within 5 minutes
    totPredictions, totFilteredPredictions = predict.getPredictions()
    total = len(predicted)
    startid = 0

#    im, file = gen.__next__()
#    count, ooi1 = predict.findboxes(file, predicted)
#    #image_new, count, ooi1, id, binary = bl.findboxes(im, startid)
#    for oi in ooi1:
#        oi.id = startid
#        startid = startid + 1

    #clas.makeprediction(im, ooi1)

    iterCount = 0
    firstTime = 1
    oldFile = ""
#    for im, file in gen:
    for insect in predicted:
        file = insect['image']
        if oldFile == file:
            oldFile = file
            continue
        else:
            oldFile = file
            
        iterCount += 1
        print('Image nr. ' + str(iterCount) + '/' + str(total), file)
        time1 = time.time()
        
        if firstTime == 1:
            firstTime = 0
            count, ooi1 = predict.findboxes(file, predicted)
            for oi in ooi1:
                oi.id = startid
                startid = startid + 1            
        
        count2, ooi2 = predict.findboxes(file, predicted)
        if count2 > 0:
            goods, startid = tr.track_boxes(ooi1, ooi2, count2, startid)
            ooi1 = goods
            #clas.makeprediction(im, goods)
            tracks.save(insect, goods)
            stat.update_stats(goods, file)
            print(stat.count)

            if writemovie:
                file_name = conf['datareader']['datapath'] + '/' + file
                im = io.imread(file_name)
                image = imod.drawoois(im, goods)
                height, width, channel = image.shape
                bytesPerLine = 3 * width
                qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        
                # Write frame
                mm.writeframe(image, file)

            time2 = time.time()
            print('Processing image took {:.3f} ms'.format((time2 - time1) * 1000.0))

    if writemovie:
        mm.releasemovie()
        
    tracks.close()
    resultdir = conf['moviemaker']['resultdir'] + '/'
    stat.writedetails(resultdir + dirName)

    return stat, resultdir, iterCount, totPredictions, totFilteredPredictions


def print_totals(date, stat, resultdir):
    record = str(date) + ','
    for spec in stat.species:
        print(spec, stat.count[spec])
        record += str(stat.count[spec]) + ','
    print('Total', stat.count['total'])
    record += str(stat.count['total']) + '\n'

    file = open(resultdir + 'statistics.csv', 'a')
    file.write(record)
    file.close()

    stat.count['date'] = date
    file = open(resultdir + 'statistics.json', 'a')
    file.write(str(stat.count) + '\n')
    file.close()


if __name__ == '__main__':

    print('STARTING NOW. Please wait.....')

    dirNames = [ 
                '20200625', 
                '20200626', 
                '20200627', 
                '20200628', 
                '20200629', 
                '20200630', 
                '20200701', 
                '20200702', 
                '20200703', 
                '20200706', 
                '20200707', 
                '20200708', 
                '20200709', 
                '20200710', 
                '20200711', 
                '20200712', 
                '20200713', 
                '20200714', 
                '20200715', 
                '20200716', 
                '20200717', 
                '20200718', 
                '20200719', 
                '20200720', 
                '20200721', 
                '20200722', 
                '20200723', 
                '20200724', 
                '20200725', 
                '20200726', 
                '20200727', 
                '20200728', 
                '20200729', 
                '20200730', 
                '20200731',
                '20200803',
                '20200804',
                '20200805',
                '20200806',
                '20200807',
                '20200808',
                '20200809',
                '20200810',
                '20200811',
                '20200812',
                '20200813', 
                '20200814', 
                '20200815', 
                '20200816',
                '20200817',
                '20200818',
                '20200819',
                '20200820',
                '20200821',
                '20200822',
                '20200823',
                '20200824',
                '20200825',
                '20200826',
                '20200827',
                '20200828',
                '20200829',
                '20200830',
                '20200901',
                '20200902',
                '20200903',
                '20200904',
                '20200905',
                '20200906',
                '20200907',
                '20200908',
                '20200909',
                '20200910',
                '20200911',
                '20200912',
                '20200913',
                '20200914',
                '20200915',
                '20200916',
                '20200917',
                '20200918',
                '20200919',
                '20200920',
                '20200921',
                '20200922',
                '20200923',
                '20200924',
                '20200925',
                '20200926',
                '20200927',
                '20200928',
                '20200929'
                ]
    
    imageCounts = 0
    totalPredictions = 0
    totalFilteredPredictions = 0
    for dirName in dirNames:
        print(dirName)
        stat, resultdir, counts, totPred, totFiltered = run(dirName)
        totalPredictions += totPred
        totalFilteredPredictions += totFiltered
        imageCounts += counts
        if dirName == '':
            date = 901
        else:    
            date = int(dirName[0:8])  # format YYYYMMDD
        print_totals(date, stat, resultdir)
        
    print(imageCounts)
    print(totalPredictions, totalFilteredPredictions, totalFilteredPredictions/totalPredictions)
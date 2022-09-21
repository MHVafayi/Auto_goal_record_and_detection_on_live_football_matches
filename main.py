# This is a sample Python script.
import time

import DataFile
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import Record
from time import sleep
import GetResults
from datetime import datetime as dt


# dataFile: list[DataFile.DataFile()] =[]
class Control:
    def __init__(self, updateSec: int, videoLen: int, UrlForCheckScore: list[str], UrlForRecord: list[str], attribute:list[str] =[] , value: list[str]=[] , tag:  list[str]=[], videoBoxAttribute:  list[str]=[] , videoBoxValue:  list[str]=[] , videoBoxTag : list[str]=[]):
        self.updatesec = updateSec
        self.videolen = videoLen
        self.dataFiles = []
        self.delay = 0
        #build data class
        for index in range(len(UrlForCheckScore)):
            try:
                dataFile = DataFile.DataFile()
                dataFile.URlTocheck = UrlForCheckScore[index]
                dataFile.URLToPlay = UrlForRecord[index]
                try:
                    dataFile.attribute = attribute[index]
                    dataFile.value = value[index]
                    dataFile.tag = tag[index]
                except:
                    pass
                try:
                    dataFile.videoBoxAttribute = videoBoxAttribute[index]
                    dataFile.videoBoxValuee = videoBoxValue[index]
                    dataFile.videoBoxTag = videoBoxTag[index]
                except:
                    pass
                dataFile.setSource()
                if len(self.dataFiles) == 0:
                    self.dataFiles.append(dataFile)
                else:
                    for n in range(len(self.dataFiles)):
                        if self.dataFiles[n].importanceLevel > dataFile.importanceLevel:
                            self.dataFiles.insert(n , dataFile)
                            break
                        elif n == len(self.dataFiles) -1 :
                            self.dataFiles.append(dataFile)
            except:
                  raise Exception("Number of urls in UrlForCheckScore should be equal to urls in UrlForRecord")
        for n in range(len(self.dataFiles)):
            print(self.dataFiles[n].URlTocheck)
        self.getResult = GetResults.GetResults(self.dataFiles)
        self.ended = False
        self.timer()

    def timer(self):
        while True:
            if (self.ended == True):
                break
            sleep(self.updatesec)
            self.getResult.updateResults()
            numOfEnded = 0
            self.delay = 0
            print("------------")
            for data in self.dataFiles:
                startTime = time.time()
                if data.minGame == "Full-Time":
                    numOfEnded += 1
                    if numOfEnded == len(self.dataFiles):
                        self.ended = True
                        break
                    endTime = time.time()
                    if endTime - startTime > 7:
                        self.delay += endTime - startTime
                    continue
                if data.isChanged:
                    Record.Record(data, self.videolen, self.delay).record()
                endTime = time.time()
                if endTime - startTime > 7:
                    self.delay += endTime - startTime
                    # elif ((int(now.strftime("%M")) - int(data.timeOfHalfTime)) + int(data.timeOfHalfTime)) < int(data.halfTimeEnd):
                    #     continue
                    # elif self.getResult.getMin() == "Half-Time":
                    #     data.timeOfHalfTime = now.strftime("%M")
                    #     data.halfTimeEnd = str(int(data.timeOfHalfTime) + 16)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    urlForCheck= ["https://www.fotmob.com/match/3784507/matchfacts/scotland-vs-ukraine"]
    urlPlay =["https://telewebion.com/live/tv3"]
    # tag =["","","","","div","div"]
    # value =["","","","","تمام صفحه","تمام صفحه"]
    # atribute =["","","","","aria-label","aria-label"]
    # print(len(urlPlay))
    # print(len(urlForCheck))
    Control(20 , 40 , urlForCheck , urlPlay )
    # datafile = DataFile.DataFile()
    # datafile.URlTocheck = "https://www.fotmob.com/match/4014853/matchfacts/hb-k%C3%B8ge-(w)-vs-juventus-(w)"
    # datafile.URLToPlay = "https://amzfootball.com/live/streaming-koge-vs-juventus-w-1629130033.html"
    # data = DataFile.DataFile()
    # data.URLToPlay = "https://telewebion.com/live/varzesh"
    # Record.Record( data, 3 , 0).record()
    #print(time.strftime("%H%M"))
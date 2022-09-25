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
    def __init__(self, updateSec: int, videoLen: int, UrlForCheckScore: list[str], UrlForRecord: list[str],
                 attribute: list[str] = [], value: list[str] = [], tag: list[str] = [],
                 videoBoxAttribute: list[str] = [], videoBoxValue: list[str] = [], videoBoxTag: list[str] = []):
        self.updatesec = updateSec
        self.videolen = videoLen
        self.dataFiles = []
        self.delay = 0
        # build data class
        for index in range(len(UrlForCheckScore)):
            try:
                dataFile = DataFile.DataFile()
                dataFile.URlTocheck = UrlForCheckScore[index]
                dataFile.URLToPlay = UrlForRecord[index]
                try:
                    dataFile.attribute = attribute[index]
                    dataFile.value = value[index]
                    dataFile.tag = tag[index]
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
                            self.dataFiles.insert(n, dataFile)
                            break
                        elif n == len(self.dataFiles) - 1:
                            self.dataFiles.append(dataFile)
            except:
                raise Exception("Number of urls in UrlForCheckScore should be equal to urls in UrlForRecord")
        for data in self.dataFiles:
            GetResults.GetResults(data).setInfoWithDecode()
            if data.minGame == "Today":
                print(data.team1 + " vs " + data.team2 + " has not started yet")
        self.timer()

    def timer(self):
        while True:
            numOfEnded = 0
            self.delay = 0
            # average time for each index in the bottom loop is 2 sec
            for data in self.dataFiles:
                startTime = time.time()
                if data.minGame == "Full-Time":
                    numOfEnded += 1
                    continue
                elif data.minGame == "Cancelled":
                    numOfEnded += 1
                    continue
                elif data.minGame == "Today":
                    startTime = time.strftime("%d") + data.result1[0:2] + data.result2[2::]
                    if int(time.strftime("%d%H%M")) > int(startTime):
                        GetResults.GetResults(data).setInfoWithDecode()
                    else:
                        continue
                elif data.minGame == "Tomorrow":
                    startTime = str(int(time.strftime("%d")) + 1) + data.result1[0:2] + data.result2[2::]
                    if int(time.strftime("%d%H%M")) > int(startTime):
                        GetResults.GetResults(data).setInfoWithDecode()
                    else:
                        continue
                else:
                    if GetResults.GetResults(data).updateResults():
                        Record.Record(data, self.videolen, self.delay).record()
                endTime = time.time()
                if int(endTime) - int(startTime) > 7:
                    self.delay += int(endTime) - int(startTime)
            if numOfEnded == len(self.dataFiles):
                break
            sleep(self.updatesec)
            print("---------")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    urlForCheck = ["some Fotmob url"]
    urlPlay = ["some url to play"]
    tag = ["", "", "", "", "div", "div"]
    value = ["", "", "", "", "تمام صفحه", "تمام صفحه"]
    atribute = ["", "", "", "", "aria-label", "aria-label"]
    #print(len(urlPlay))
    #print(len(urlForCheck))
    Control(20, 40, urlForCheck, urlPlay)


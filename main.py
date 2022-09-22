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
                        print(data.team1 + " vs " + data.team2 + " has not started yet")
                        continue
                elif data.minGame == "Tomorrow":
                    startTime = str(int(time.strftime("%d")) + 1) + data.result1[0:2] + data.result2[2::]
                    if int(time.strftime("%d%H%M")) > int(startTime):
                        GetResults.GetResults(data).setInfoWithDecode()
                    else:
                        print(data.team1 + " vs " + data.team2 + " has not started yet")
                        continue
                else:
                    if GetResults.GetResults(data).updateResults():
                        Record.Record(data, self.videolen, self.delay).record()
                endTime = time.time()
                if endTime - startTime > 7:
                    self.delay += endTime - startTime
            if numOfEnded == len(self.dataFiles):
                break
            sleep(self.updatesec)
            print("---------")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    urlForCheck = ["https://www.fotmob.com/match/3784584/matchfacts/belgium-vs-wales",
                   "https://www.fotmob.com/match/3784519/matchfacts/france-vs-austria",
                   "https://www.fotmob.com/match/3784585/matchfacts/poland-vs-netherlands",
                   "https://www.fotmob.com/match/3784518/matchfacts/croatia-vs-denmark",
                   "https://www.fotmob.com/match/3784548/matchfacts/lithuania-vs-faroe-islands",
                   "https://www.fotmob.com/match/3784549/matchfacts/turkiye-vs-luxembourg",
                   "https://www.fotmob.com/match/3784621/matchfacts/slovakia-vs-azerbaijan",
                   "https://www.fotmob.com/match/3784646/matchfacts/liechtenstein-vs-andorra"]
    urlPlay = ["https://telewebion.com/live/varzesh",
               "https://telewebion.com/live/twsport",
               "https://www.anten.ir/program/47221/%D9%81%D9%88%D8%AA%D8%A8%D8%A7%D9%84-%D9%84%D9%87%D8%B3%D8%AA%D8%A7%D9%86-%D9%87%D9%84%D9%86%D8%AF",
               "https://www.anten.ir/program/47224/%D9%81%D9%88%D8%AA%D8%A8%D8%A7%D9%84-%DA%A9%D8%B1%D9%88%D8%A7%D8%B3%DB%8C-%D8%AF%D8%A7%D9%86%D9%85%D8%A7%D8%B1%DA%A9",
               "https://amzfootball.com/live/streaming-lithuania-vs-faroe-islands-1629114909.html",
               "https://amzfootball.com/live/streaming-turkey-vs-luxembourg-1629114910.html",
               "https://amzfootball.com/live/streaming-slovakia-vs-azerbaijan-1629114911.html",
               "https://amzfootball.com/live/streaming-liechtenstein-vs-andorra-1629114912.html"]
    tag = ["1", "", "", "", "div", "div"]
    value = ["2", "", "", "", "تمام صفحه", "تمام صفحه"]
    atribute = ["3", "", "", "", "aria-label", "aria-label"]
    # print(len(urlPlay))
    # print(len(urlForCheck))
    #Control(20, 40, urlForCheck, urlPlay)
    datafile = DataFile.DataFile()
    datafile.URlTocheck = "https://www.fotmob.com/match/4014853/matchfacts/hb-k%C3%B8ge-(w)-vs-juventus-(w)"
    datafile.URLToPlay = "https://telewebion.com/live/twsport"
    datafile.setSource()
    # # data = DataFile.DataFile()
    # # data.URLToPlay = "https://telewebion.com/live/varzesh"
    Record.Record( datafile, 3 , 0).record()
    # print(time.strftime("%H%M"))

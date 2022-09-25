# This is a sample Python script.
import time

import DataFile
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import Record
from time import sleep
import GetResults
from datetime import datetime as dt


class Control:
    def __init__(self, updateSec: int, videoLen: int, UrlForCheckScore: list[str], UrlForRecord: list[str],
                 fullScreenXPATH: list[str] = [],resumeXPATH: list[str] = [] , timeTORewind :int = 45):
        """
              if you want to record in Full-Screen either you must choose one of the these websites: telewebion, aparat, anten
        or you should give some information about Full Screen button from inspect in the website like attribute = 'aria-label' , value = 'Full Screen' , tag ='button'
        also if you need you can pass resume button attributes

        parameters:
            :param updateSec: timespan in seconds to check results
            :param videoLen: record time length
            :param UrlForCheckScore: a 'Fotmob' url to check results
            :param UrlForRecord: a url to record
            :param fullScreenXPATH: XPATH of fullScreen button if website wasnt in my code
            :param resumeXPATH: if website needed to resume video
            :param timeTORewind: timespan in seconds to rewind video if you use a website that lets you do so
        """
        self.updatesec = updateSec
        self.videolen = videoLen
        self.dataFiles = []
        self.delay = 0
        self.timeToRewind = timeTORewind
        # build data classes
        for index in range(len(UrlForCheckScore)):
            try:
                dataFile = DataFile.DataFile()
                dataFile.URlTocheck = UrlForCheckScore[index]
                dataFile.URLToPlay = UrlForRecord[index]
                try:
                    dataFile.fullScreenXPATH = fullScreenXPATH[index]
                except:
                    pass
                try:
                    dataFile.resumeXPATH = resumeXPATH[index]
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
                        Record.Record(data, self.videolen, self.delay, self.timeToRewind).record()
                endTime = time.time()
                self.delay += int(endTime) - int(startTime)
            if numOfEnded == len(self.dataFiles):
                break
            sleep(self.updatesec)
            print("---------")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    urlForCheck = [
        "https://www.fotmob.com/match/3784520/matchfacts/austria-vs-croatia",
    "https://www.fotmob.com/match/3784586/matchfacts/netherlands-vs-belgium",
    "https://www.fotmob.com/match/3784521/matchfacts/denmark-vs-france",
    "https://www.fotmob.com/match/3784587/matchfacts/wales-vs-poland",
    "https://www.fotmob.com/match/3784587/matchfacts/wales-vs-poland",
    "https://www.fotmob.com/match/3784521/matchfacts/denmark-vs-france",
    "https://www.fotmob.com/match/3784550/matchfacts/faroe-islands-vs-turkiye",
    "https://www.fotmob.com/match/3784551/matchfacts/luxembourg-vs-lithuania"]
    urlPlay = ["https://www.anten.ir/program/47271/%D9%81%D9%88%D8%AA%D8%A8%D8%A7%D9%84-%D8%A7%D8%AA%D8%B1%DB%8C%D8%B4-%DA%A9%D8%B1%D9%88%D8%A7%D8%B3%DB%8C",
                "https://telewebion.com/live/tv3",
               "https://telewebion.com/live/varzesh",
               "https://telewebion.com/live/twsport",
               "https://www.anten.ir/program/47266/%D9%81%D9%88%D8%AA%D8%A8%D8%A7%D9%84-%D9%88%D9%84%D8%B2-%D9%84%D9%87%D8%B3%D8%AA%D8%A7%D9%86",
               "https://www.aparat.com/AparatSport/live",
               "https://amzfootball.com/live/streaming-faroe-islands-vs-turkey-1629115037.html",
               "https://amzfootball.com/live/streaming-luxembourg-vs-lithuania-1629115038.html"]
    print(len(urlPlay))
    print(len(urlForCheck))
    #at = ["//button[@class='vjs-fullscreen-control vjs-control vjs-button']"]
    #re=["//button[@aria-label='پخش K']"]
    Control(20, 45, urlForCheck, urlPlay)
    datafile = DataFile.DataFile()
    datafile.URlTocheck = "https://www.fotmob.com/match/4014853/matchfacts/hb-k%C3%B8ge-(w)-vs-juventus-(w)"
    datafile.URLToPlay = "https://www.namasha.com/v/nfmvDDLg"

    datafile.setSource()
    # # # data = DataFile.DataFile()
    # # # data.URLToPlay = "https://telewebion.com/live/varzesh"
    #Record.Record(datafile, 35, 0).record()
    # print(time.strftime("%H%M"))

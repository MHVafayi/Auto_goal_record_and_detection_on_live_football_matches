# This is a sample Python script.
import time
import DataFile
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import Record
from time import sleep
import GetResults


class Control:
    def __init__(self, updateSec: int, videoLen: int, UrlForCheckScore: list[str], UrlForRecord: list[str],
                 fullScreenXPATH: list[str] = [], resumeXPATH: list[str] = [], timeTORewind: int = 45):
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
            GetResults.GetResults(data).setAll()
            if data.minGame == "Today":
                startHour = str(data.startTime)
                while len(startHour) < 4:
                    startHour = "0"+startHour
                print(data.team1 + " vs " + data.team2 + " starts at " + startHour[0:2] + ":" + startHour[2::])
            elif data.minGame == "Cancelled":
                print(data.team1 + " vs " + data.team2 + " has been cancelled")
            elif data.minGame == "Full-Time":
                print(data.team1 + " vs " + data.team2 +" is over")
            elif data.minGame == "Half-Time":
                pass
            elif data.minGame.find(":") == -1:
                startHour = str(data.startTime)
                while len(startHour) < 4:
                    startHour = "0"+startHour
                print(data.team1 + " vs " + data.team2 +" starts on " + data.matchDay +" at "+ startHour[0:2] + ":" + startHour[2::])

        self.timer()

    def timer(self):
        while True:
            numOfEnded = 0
            self.delay = 0
            for data in self.dataFiles:
                startTime = time.time()
                if data.minGame == "Full-Time":
                    numOfEnded += 1
                elif data.minGame == "Cancelled":
                    numOfEnded += 1
                elif data.minGame == "Half-Time":
                    now = int(time.strftime("%H%M"))
                    if now >= data.estimatedEndOfHalfTime:
                        GetResults.GetResults(data).setMutableData()
                elif data.minGame.find(":") != -1:
                    if GetResults.GetResults(data).updateResults():
                        Record.Record(data, self.videolen, self.delay + int(time.time() - startTime),
                                      self.timeToRewind).record()
                else:
                    today = time.strftime("%b %#d %Y")
                    now = int(time.strftime("%H%M"))
                    if today == data.matchDay and now >= data.startTime:
                        GetResults.GetResults(data).setMutableData(True)
                endTime = time.time()
                self.delay += endTime - startTime
            if numOfEnded == len(self.dataFiles):
                break
            sleep(self.updatesec)
            print("---------")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    urlForCheck = []
    urlPlay = []
    # print(len(urlPlay))
    # print(len(urlForCheck))
    Control(20, 45, urlForCheck, urlPlay)



from math import gcd
import validators
import DataFile
import Record
from time import sleep, time, strftime
import GetResults
from Other import AskMe


def setProfile(FirefoxProfilePath: str):
    # it saves path of Firefox profile by writing in profile.txt
    profile = open("Profile.txt", 'w')
    profile.write("FirefoxProfilePath: " + FirefoxProfilePath)


class Control:
    def __init__(self, syncDuration: int, videoLen: int, UrlForCheckScore: list[str], UrlForRecord: list[str],
                 fullScreenXPATH: list[str] = [], resumeXPATH: list[str] = [], timeToRewind: int = 30,
                 FirefoxProfile: str = ""):
        """
            It processes all the classes in this project in order to check and record goals of the games.
    It's good to know that if you want to record in full screen, you must either choose one of the following websites:
    Telewebion, Aparat, or Anten, or you must enter the XPath of full screen or resume buttons.
            :param syncDuration: duration, in seconds, for checking results
            :param videoLen: record duration, in seconds
            :param UrlForCheckScore: 'Fotmob' urls for checking results
            :param UrlForRecord: urls for recording goals
            :param fullScreenXPATH: For the purpose of recoding goals from other websites that I didn't write in my
            code,if you want you can enter XPaths of full screen buttons in a list with a length of other websites than
            Telewebion, Aparat, and Anten in UrlForRecord. It's important to note that you only need to enter in order
            that you entered it in UrlForRecord.
            :param resumeXPATH: same thing as fullScreenXPATH
            :param timeToRewind: Timespan in seconds to rewind video, just have use in Telewebion urls
            :param FirefoxProfile: If you want to open your profile in Firefox after using it once, it saves the path so
             you don't have to enter it each time until the path changes. 
        """
        self.updateSecChunk = syncDuration
        self.updateSec = syncDuration
        self.videoLen = videoLen
        self.dataFiles = []
        self.uncompletedDataFiles = []
        self.delay = self.doesntWorkRightNow = self.numOfEnded = 0
        self.timeToRewind = timeToRewind
        self.limit = self.counter = 1
        if FirefoxProfile != "":
            setProfile(FirefoxProfile)
        # build data classes
        for index in range(len(UrlForCheckScore)):
            dataFile = DataFile.DataFile()
            dataFile.UrlToCheck = UrlForCheckScore[index]
            GetResults.GetResults(dataFile).setAll()
            try:
                if isinstance(UrlForRecord[index], AskMe):
                    dataFile.UrlToPlay = "wait"
                    dataFile.askForUrl(UrlForRecord[index])
                    self.uncompletedDataFiles.append(dataFile)
                else:
                    url = UrlForRecord[index]
                    while not validators.url(url):
                        print("the " + dataFile.team1 + " vs " + dataFile.team2 + "'s url isn't valid")
                        url = input("enter a url:")
                    dataFile.UrlToPlay = url
            except IndexError:
                dataFile.UrlToPlay = "wait"
                dataFile.askForUrl(AskMe.LATER)
                self.uncompletedDataFiles.append(dataFile)

            dataFile.setSource()
            if dataFile.source == "unknown":
                try:
                    dataFile.fullScreenXPath = fullScreenXPATH[0]
                    del fullScreenXPATH[0]
                except:
                    pass
                try:
                    dataFile.resumeXPath = resumeXPATH[0]
                    del fullScreenXPATH[0]
                except:
                    pass
            self.addAndSortList(dataFile)

    def start(self):  # it errors on dosent have url
        # if some matches was finished or was in Half-Time show it once
        for dataFile in self.dataFiles:
            if dataFile.minGame == "Today":
                startHour = str(dataFile.startTime)
                print(
                    dataFile.team1 + " vs " + dataFile.team2 + " starts at " + startHour[8:10] + ":" + startHour[10::])
            elif dataFile.minGame == "Cancelled":
                print(dataFile.team1 + " vs " + dataFile.team2 + " has been cancelled")
            elif dataFile.minGame == "Full-Time" or dataFile.minGame == "Half-Time" or dataFile.minGame == "Awarded win":
                print(dataFile.resultToString())
            elif dataFile.minGame.find(":") == -1:
                startHour = str(dataFile.startTime)
                print(
                    dataFile.team1 + " vs " + dataFile.team2 + " starts on " + dataFile.getDateOfTheGame() + " at " + startHour[
                                                                                                                   8:10] + ":" + startHour[
                                                                                                                                 10::])
        if len(self.uncompletedDataFiles) > 0 and self.updateSecChunk > 60:
            self.__setCounter()
        # to divide UpdateSec into smaller pieces because if it was greater than 60 it would make some troubles for askForUrl
        while self.numOfEnded < len(self.dataFiles):
            isWorking = self.doesntWorkRightNow + self.numOfEnded < len(self.dataFiles)
            if self.counter == self.limit:
                self.checkAll()
                self.counter = 1
                if self.numOfEnded == len(self.dataFiles):
                    break
                if isWorking:
                    print("---------")
            else:
                self.counter += 1
            begin = time()
            self.askForUrl()
            end = time()
            # to make it faster by remove respond time in askForUrl
            Chunk = self.updateSecChunk - (end - begin)
            if Chunk > 0:
                sleep(Chunk)

    def checkAll(self):
        """
            review every match result, and if any of them were changed, record the goal.
        """
        # check each data in dataFiles
        self.numOfEnded = 0
        self.delay = 0
        self.doesntWorkRightNow = 0
        for data in self.dataFiles:
            startTime = time()
            if data.minGame == "Full-Time" or data.minGame == "Cancelled" or data.minGame == "Awarded win":
                self.numOfEnded += 1
            elif data.minGame == "Half-Time":
                self.doesntWorkRightNow += 1
                now = int(strftime("%Y%m%d%H%M"))
                if now >= data.estimatedEndOfHalfTime:
                    GetResults.GetResults(data).setMutableData()
            elif data.minGame.find(":") != -1:
                if GetResults.GetResults(data).hasResultChanged():
                    Record.Record(data, self.videoLen, self.delay + int(time() - startTime),
                                  self.timeToRewind).record()
            else:
                self.doesntWorkRightNow += 1
                now = int(strftime("%Y%m%d%H%M"))
                if now >= data.startTime:
                    GetResults.GetResults(data).setMutableData(True)
            endTime = time()
            self.delay += endTime - startTime

    def askForUrl(self):
        for UData in self.uncompletedDataFiles:
            if UData.minGame == "Full-Time" or UData.minGame == "Cancelled" or UData.minGame == "Awarded win" :
                # because it has finished
                continue
            if int(strftime("%Y%m%d%H%M")) >= UData.waitUntil:
                print("!!-------")
                print("please enter the " + UData.team1 + " vs " + UData.team2+"'s url for recording goals")
                print("if you don't have it again write one of this options : 1- Later 2- When the match starts "
                      "3- Before the match starts 4-Delete this match 5-Exit")
                x = str(input()).strip()
                if x.lower().find("before") != -1 and x.find(".") == -1 or x == "3":
                    UData.askForUrl(AskMe.BEFORE_THE_MATCH_STARTS)
                elif x.lower().find("later") != -1 and x.find(".") == -1 or x == "1":
                    UData.askForUrl(AskMe.LATER)
                elif x.lower().find("start") != -1 and x.find(".") == -1 or x == "2":
                    UData.askForUrl(AskMe.WHEN_THE_MATCH_STARTS)
                elif x.lower().find("delete") != -1 and x.find(".") == -1 or x == "4":
                    self.dataFiles.remove(UData)
                    self.uncompletedDataFiles.remove(UData)
                elif x.lower().find("exit") != -1 and x.find(".") == -1 or x == "5":
                    raise SystemExit(0)
                else:
                    if validators.url(x):
                        UData.UrlToPlay = x
                        UData.setSource()
                        if UData.source == "unknown" :
                            FXPATH = str(input("XPATH of FullScreen button if you want otherwise write 'skip': ")).strip()
                            RXPATH = str(input("XPATH of Resume button if you want otherwise write 'skip': ")).strip()
                            if FXPATH.lower() != "skip":
                                UData.fullScreenXPath = FXPATH
                                UData.source += "+FullScreen"
                            if RXPATH.lower() != "skip":
                                UData.resumeXPath = RXPATH
                                UData.source += "+Resume"
                        self.dataFiles.remove(UData)
                        self.addAndSortList(UData)
                        self.uncompletedDataFiles.remove(UData)
                        if len(self.uncompletedDataFiles) == 0:
                            self.updateSecChunk = self.updateSec
                            self.limit = 1
                            self.counter = 1
                    else:
                        print("the url isn't valid")
                        self.askForUrl()
                        return
                print("!!---------")

    def addAndSortList(self, dataFile: DataFile.DataFile):
        if len(self.dataFiles) == 0:
            self.dataFiles.append(dataFile)
        else:
            for n in range(len(self.dataFiles)):
                if self.dataFiles[n].importanceLevel > dataFile.importanceLevel:
                    self.dataFiles.insert(n, dataFile)
                    break
                elif n == len(self.dataFiles) - 1:
                    self.dataFiles.append(dataFile)

    def __setCounter(self):
        while True:
            sleepGCD = gcd(60, self.updateSecChunk)
            if sleepGCD >= 10:
                self.limit = self.counter = self.updateSecChunk / sleepGCD
                self.updateSecChunk = sleepGCD
                break
            self.updateSecChunk -= 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    urlForCheck = []
    urlPlay = []
    # print(len(urlPlay))
    # print(len(urlForCheck))
    Control(30, 60, urlForCheck, urlPlay).start()


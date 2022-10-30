from math import gcd
import validators
from GoalRecorder.src import DataFile, GetResults, Record
from time import sleep, time, strftime
from GoalRecorder.src.Other import AskMe


class Control:
    def __init__(self, UrlForCheckScore: list[str], UrlForRecord: list[str]):
        """
            It processes all the classes in this project in order to check and record goals of the games.
    It's good to know that if you want to record in full screen, you must either choose one of the following websites:
    Telewebion, Aparat, or Anten, or you must enter the XPath of full screen or resume buttons.
            :param UrlForCheckScore: 'Fotmob' urls for checking results
            :param UrlForRecord: urls for recording goals
        """
        print("-------------")
        try:
            profile = open("GoalRecorder/src/Profile.txt", 'r', encoding="utf-8")
        except:
            profile = open("src/Profile.txt", 'r', encoding="utf-8")
        for line in profile:
            if line.find("FirefoxProfilePath:") != -1:
                self.profile = line[line.find("FirefoxProfilePath:") + len("FirefoxProfilePath:")::].strip()
            elif line.find("syncDuration:") != -1:
                self.updateSec = self.updateSecChunk = int(line[line.find("syncDuration:") + len("syncDuration:")::].strip())
            elif line.find("videoLen:") != -1:
                self.videoLen = int(line[line.find("videoLen:") + len("videoLen:")::].strip())
            elif line.find("rewindTime:") != -1:
                self.timeToRewind = int(line[line.find("rewindTime:") + len("rewindTime:")::].strip())
        profile.close()
        self.dataFiles = []
        self.uncompletedDataFiles = []
        self.delay = self.doesntWorkRightNow = 0
        self.limit = self.counter = 1
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

            dataFile.setAll()
            self.addAndSortList(dataFile)

    def start(self):
        # if some matches was finished or was in Half-Time show it once
        for dataFile in reversed(self.dataFiles):
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
        while len(self.dataFiles) > 0:
            isWorking = self.doesntWorkRightNow < len(self.dataFiles)
            if self.counter == self.limit:
                self.checkAll()
                self.counter = 1
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
        self.delay = 0
        self.doesntWorkRightNow = 0
        for data in reversed(self.dataFiles):
            startTime = time()
            if data.minGame == "Full-Time" or data.minGame == "Cancelled" or data.minGame == "Awarded win":
                self.dataFiles.remove(data)
            elif data.minGame == "Half-Time":
                self.doesntWorkRightNow += 1
                now = int(strftime("%Y%m%d%H%M"))
                if now >= data.estimatedEndOfHalfTime:
                    GetResults.GetResults(data).setMutableData()
            elif data.minGame.find(":") != -1:
                if GetResults.GetResults(data).hasResultChanged():
                    Record.Record(data, self.videoLen, self.delay + int(time() - startTime),
                                  self.timeToRewind, self.profile).record()
            else:
                self.doesntWorkRightNow += 1
                now = int(strftime("%Y%m%d%H%M"))
                if now >= data.startTime:
                    GetResults.GetResults(data).setMutableData(possibleScheduleChanges=True)
            endTime = time()
            self.delay += endTime - startTime

    def askForUrl(self):
        for UData in reversed(self.uncompletedDataFiles):
            if UData.minGame == "Full-Time" or UData.minGame == "Cancelled" or UData.minGame == "Awarded win":
                # because it has finished
                self.uncompletedDataFiles.remove(UData)
                continue
            if int(strftime("%Y%m%d%H%M")) >= UData.waitUntil:
                print("!!-------")
                print("please enter the " + UData.team1 + " vs " + UData.team2 + "'s url for recording goals")
                print("if you don't have it again write one of this options : 1- Later 2- When the match starts "
                      "3- Before the match starts 4-Delete this match 5-Exit")
                while True:
                    x = str(input()).strip()
                    if x.lower().find("before") != -1 and x.find(".") == -1 or x == "3":
                        UData.askForUrl(AskMe.BEFORE_THE_MATCH_STARTS)
                        break
                    elif x.lower().find("later") != -1 and x.find(".") == -1 or x == "1":
                        UData.askForUrl(AskMe.LATER)
                        break
                    elif x.lower().find("start") != -1 and x.find(".") == -1 or x == "2":
                        UData.askForUrl(AskMe.WHEN_THE_MATCH_STARTS)
                        break
                    elif x.lower().find("delete") != -1 and x.find(".") == -1 or x == "4":
                        self.dataFiles.remove(UData)
                        self.uncompletedDataFiles.remove(UData)
                        break
                    elif x.lower().find("exit") != -1 and x.find(".") == -1 or x == "5":
                        raise SystemExit(0)
                    else:
                        if validators.url(x):
                            UData.UrlToPlay = x
                            UData.setAll()
                            self.dataFiles.remove(UData)
                            self.addAndSortList(UData)
                            self.uncompletedDataFiles.remove(UData)
                            if len(self.uncompletedDataFiles) == 0:
                                self.updateSecChunk = self.updateSec
                                self.limit = 1
                                self.counter = 1
                            break
                        else:
                            print("the url isn't valid")
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



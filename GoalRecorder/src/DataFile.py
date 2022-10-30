from time import strftime
from urllib.parse import urlparse
from GoalRecorder.src.Other import AskMe, sumTwoTimes, minusTwoTimes


class DataFile:
    def __init__(self):
        self.UrlToPlay = ""
        self.UrlToCheck = ""
        self.team1 = "unknown1"
        self.team2 = "unknown2"
        self.minGame = "00:00"
        self.result1 = ""
        self.result2 = ""
        self.source = "unknown.unk!:"
        self.fullScreenXPath = ""
        self.resumeXPath = ""
        self.importanceLevel = -1
        self.startTime = 0
        self.estimatedEndOfHalfTime = 100
        self.waitUntil = 0
        self.choice = None
        self.timeLabelXPath = ""
        self.progressBarXPath = ""

    def getFileName(self):
        return self.team1 + self.result1 + "-" + self.result2 + self.team2 + self.minGame[0:self.minGame.find(":")]

    def resultToString(self):
        return self.team1 + " " + self.result1 + " - " + self.result2 + " " + self.team2 + " " + self.minGame

    def setImportanceLevel(self):
        try:
            stream = open("GoalRecorder/src/StreamWebsites.txt", 'r', encoding="utf-8")
        except:
            stream = open("src/StreamWebsites.txt", 'r', encoding="utf-8")
        for line in stream:
            if line.find(self.source) != -1:
                self.importanceLevel = int(line[line.find("importance") + len("importance:")::].strip())
                break
        if self.importanceLevel == -1:
            self.importanceLevel = 0

    def setSource(self):
        self.source = str(urlparse(self.UrlToPlay).netloc)

    def setElementsXPath(self):
        try:
            stream = open("GoalRecorder/src/StreamWebsites.txt", 'r', encoding="utf-8")
        except:
            stream = open("src/StreamWebsites.txt", 'r', encoding="utf-8")
        nowIn = False
        for line in stream:
            if line.strip().find(self.source+":") != -1:
                nowIn = True
            elif nowIn:
                if line.strip().find("FullScreen:") != -1:
                    self.fullScreenXPath = line[line.find("FullScreen:") + len("FullScreen: ")::].strip()
                elif line.strip().find("Resume:") != -1:
                    self.resumeXPath = line[line.find("Resume:") + len("Resume: ")::].strip()
                elif line.strip().find("TimeLabel:") != -1:
                    self.timeLabelXPath = line[line.find("TimeLabel:") + len("TimeLabel: ")::].strip()
                elif line.strip().find("ProgressBar:") != -1:
                    self.progressBarXPath = line[line.find("ProgressBar:") + len("ProgressBar: ")::].strip()
                else:
                    nowIn = False

    def setAll(self):
        self.setSource()
        self.setImportanceLevel()
        self.setElementsXPath()

    def askForUrl(self, when: AskMe):
        if self.minGame == "Full-Time" or self.minGame == "Cancelled" or self.minGame == "Awarded win":
            return
        self.choice = when
        if when.value == 0:
            self.waitUntil = self.startTime
        elif when.value == -1 and self.minGame.find(":") == -1:
            print("how many minutes before start of " + self.team1 + " vs " + self.team2 + " should i ask for url?")
            x = int(input("enter a number smaller than 1440: "))
            if x >= 1440:
                raise Exception("minutes should be smaller than 1440 but you entered " + str(x))
            hours = str(int(x / 60))
            mins = str(x % 60)
            while len(hours) < 2:
                hours = "0" + hours
            while len(mins) < 2:
                mins = "0" + mins
            print(str(hours) + str(mins))
            self.waitUntil = int(minusTwoTimes(str(self.startTime), str(hours) + str(mins)))
            print(self.startTime)
            print(self.waitUntil)
        elif when.value == 1:
            print("how many minutes later should i ask for url of " + self.team1 + " vs " + self.team2 + " ?")
            x = int(input("enter a number smaller than 1440: "))
            if x >= 1440:
                raise Exception("minutes should be smaller than 1440 but you entered " + str(x))
            hours = int(x / 60)
            mins = int(x % 60)
            self.waitUntil = int(sumTwoTimes(strftime("%Y%m%d%H%M"), str(hours) + str(mins)))

    def getDateOfTheGame(self):
        startTime = str(self.startTime)
        return startTime[0:4] + "." + startTime[4:6] + "." + startTime[6:8]

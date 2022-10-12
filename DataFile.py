from time import strftime
from urllib.parse import urlparse
import Other


class DataFile:
    def __init__(self):
        self.UrlToPlay = ""
        self.UrlToCheck = ""
        self.team1 = "unknown1"
        self.team2 = "unknown2"
        self.minGame = "00:00"
        self.result1 = ""
        self.result2 = ""
        self.source = ""
        self.fullScreenXPath = ""
        self.resumeXPath = ""
        self.importanceLevel = -1
        self.startTime = 0
        self.estimatedEndOfHalfTime = 100
        self.waitUntil = 0
        self.choice = None

    def getFileName(self):
        return self.team1 + self.result1 + "-" + self.result2 + self.team2 + self.minGame[0:self.minGame.find(":")]

    def resultToString(self):
        return self.team1 + " " + self.result1 + " - " + self.result2 + " " + self.team2 + " " + self.minGame

    def setSource(self):
        self.source = str(urlparse(self.UrlToPlay).netloc)
        if self.source == "telewebion.com":
            self.importanceLevel = 3
        elif self.source == "www.aparat.com":
            self.importanceLevel = 2
        elif self.source == "amzfootball.com":
            self.importanceLevel = 0
        elif self.source == "www.anten.ir":
            self.importanceLevel = 1
        else:
            self.source = "unknown"
            self.importanceLevel = 4
            if self.resumeXPath != "":
                self.source += "+Resume"
            if self.fullScreenXPath != "":
                self.source += "+FullScreen"

    def askForUrl(self, when: Other.AskMe):
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
            print(str(hours)+str(mins))
            self.waitUntil = int(Other.minusTwoTimes(str(self.startTime), str(hours)+str(mins)))
            print(self.startTime)
            print(self.waitUntil)
        elif when.value == 1:
            print("how many minutes later should i ask for url of " + self.team1 + " vs " + self.team2 + " ?")
            x = int(input("enter a number smaller than 1440: "))
            if x >= 1440:
                raise Exception("minutes should be smaller than 1440 but you entered " + str(x))
            hours = int(x / 60)
            mins = int(x % 60)
            self.waitUntil = int(Other.sumTwoTimes(strftime("%Y%m%d%H%M"), str(hours)+str(mins)))

    def getDateOfTheGame(self):
        startTime = str(self.startTime)
        return startTime[0:4]+"."+startTime[4:6]+"."+startTime[6:8]
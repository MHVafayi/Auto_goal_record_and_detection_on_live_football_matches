from urllib.parse import urlparse


class DataFile:
    def __init__(self):
        self.URLToPlay = ""
        self.URlTocheck = ""
        self.team1 = "unknown1"
        self.team2 = "unknown2"
        self.minGame = "00:00"
        self.result1 = ""
        self.result2 = ""
        self.source = ""
        self.fullScreenXPATH = ""
        self.resumeXPATH = ""
        self.importanceLevel = -1
        self.startTime = 0
        self.estimatedEndOfHalfTime = 100
        self.isStarted = False
        self.matchDay = "M #D Y"

    def getFileName(self):
        return self.team1 + self.result1 + "-" + self.result2 + self.team2 + self.minGame[0:self.minGame.find(":")]

    def resultToString(self):
        return self.team1 + " " + self.result1 + " - " + self.result2 + " " + self.team2 + " " + self.minGame

    def setSource(self):
        self.source = str(urlparse(self.URLToPlay).netloc)
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
            if self.resumeXPATH != "":
                self.source += "+Resume"
            if self.fullScreenXPATH != "":
                self.source += "+FullScreen"

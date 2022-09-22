import time


class DataFile:
    def __init__(self):
        self.URLToPlay = ""
        self.URlTocheck = ""
        self.team1 = "unknown1"
        self.team2 = "unknown2"
        self.minGame = "00:00"
        self.result1 = ""
        self.result2 = ""
        self.isChanged = False
        self.source =""
#        self.startOfHalfTime = 0
        self.attribute= ""
        self.value= ""
        self.tag =""
        self.videoBoxAttribute =""
        self.videoBoxValue =""
        self.videoBoxTag =""
        self.importanceLevel =-1

    def getFileName(self):
        return self.team1 + self.result1 + "-" + self.result2 + self.team2 + self.minGame[0:self.minGame.find(":")]

    def resultToString(self):
        return self.team1 + " " + self.result1 + " - " + self.result2 + " " + self.team2 + " " + self.minGame
    def setSource(self):
        if self.URLToPlay.find("telewebion") != -1:
            self.source = "telewebion"
            self.importanceLevel = 3
        elif self.URLToPlay.find("aparat") != -1:
            self.source = "aparat"
            self.importanceLevel = 2
        elif self.URLToPlay.find("amzfootball") != -1:
            self.source = "amzfootball"
            self.importanceLevel = 0
        elif self.URLToPlay.find("anten") != -1:
            self.source = "anten"
            self.importanceLevel = 1
        else:
            print(
                "if you want to record in Full-Screen either you must choose one of the default websites :\n\t-telewebion\n\t-aparat\n\t-anten")
            print(
                "or you should give some information about Full Screen button from inspect in the website like attribute = 'aria-label' , value = 'Full Screen' , tag ='button'")
            print(
                "also if Full-Screen button is unstable and would be gone after few seconds you have to pass videoBoxAttribute , videoBoxValue , videoBoxTag beside of attribute ,value and tag of Full-Screen button")
            if self.videoBoxAttribute != "" and self.videoBoxValue != "":
                if self.attribute == "" or self.value == "":
                    raise Exception(
                        "you didn't pass value or attribute or tag of Full-Screen button in parameter ('attribute', 'value' ,'tag')")
                self.source = "unknown and Full-Screen button is unstable"
                self.importanceLevel = 4
            elif self.attribute != "" and self.value != "":
                self.source = "unknown"
                self.importanceLevel =4
            else:
                pass
                #raise Exception("something is missing read the text above carefully")
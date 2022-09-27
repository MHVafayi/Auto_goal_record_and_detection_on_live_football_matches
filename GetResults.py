import time
from urllib.request import urlopen
import DataFile
from datetime import datetime, timedelta


class GetResults:
    def __init__(self, data: DataFile.DataFile()):
        self.data = data
        html = urlopen(self.data.URlTocheck).read()
        self.text = html.decode("utf-8")

    def updateResults(self):
        oldResult1 = self.data.result1
        oldResult2 = self.data.result2
        self.setMutableData()
        print(self.data.resultToString())
        if self.data.result1 != oldResult1 or self.data.result2 != oldResult2:
            return True
        else:
            return False

    def setAll(self):
        self.setImmutableData()
        self.setMutableData()
        self.setStartTime()

    def setMutableData(self, possibleToChangeTime: bool = False):
        resultScript = self.text.find('class="css-bw7eig-topRow"')
        result = self.text[
                 resultScript + len('class="css-bw7eig-topRow>"'): resultScript + self.text[resultScript:-1].find(
                     "</span>")]
        self.data.result1 = result[0:result.find("-") - 1]
        self.data.result2 = result[result.find("-") + 2::]
        minScriptIndex = self.text.find('class="css-lv1jm0-bottomRow"')
        self.data.minGame = self.text[
                            minScriptIndex + len('class="css-lv1jm0-bottomRow">'): self.text[minScriptIndex:-1].find(
                                "</span>") + minScriptIndex]
        if possibleToChangeTime:
            self.setStartTime()

    def setImmutableData(self):
        team1ScriptIndex = self.text.find('class="css-er0nau-TeamName e3q4wbq4"')
        self.data.team1 = self.text[team1ScriptIndex + len('class="css-er0nau-TeamName e3q4wbq4"><span>'):self.text[
                                                                                                          team1ScriptIndex:-1].find(
            "</span>") + team1ScriptIndex]
        team2ScriptIndex = self.text.find('class="css-11064rk-TeamMarkup-applyHover e3q4wbq5"><div '
                                          'style="width:50px;height:50px;background-color:transparent"></div><span '
                                          'class="css-er0nau-TeamName e3q4wbq4"><span>')
        self.data.team2 = self.text[team2ScriptIndex + len('class="css-11064rk-TeamMarkup-applyHover e3q4wbq5"><div '
                                                           'style="width:50px;height:50px;background-color:transparent'
                                                           '"></div><span class="css-er0nau-TeamName '
                                                           'e3q4wbq4"><span>'):self.text[team2ScriptIndex:-1].find(
            "</span>") + team2ScriptIndex]

    def setStartTime(self):
        startTimeIndex = self.text.find('<time')
        dateScript = self.text[startTimeIndex:-1]
        self.data.matchDay = dateScript[dateScript.find("<span>") + len("<span>day, "): dateScript.find("</span>")]
        dateScript = dateScript[dateScript.find("</span>") + len("</span>")::]
        self.data.startTime = int(dateScript[dateScript.find("<span>") + len("<span> "): dateScript.find("</span>")].replace(":",""))
        self.data.estimatedEndOfHalfTime = self.data.startTime + 100  # 1 hour

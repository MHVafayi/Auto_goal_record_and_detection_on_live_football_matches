from urllib.request import urlopen
from GoalRecorder.src import DataFile
from GoalRecorder.src.Other import sumTwoTimes, minusTwoTimes
import html

class GetResults:
    def __init__(self, data: DataFile.DataFile()):
        self.data = data
        try:
            htmlText = urlopen(self.data.UrlToCheck, timeout=10).read()
        except:
            htmlText = urlopen(self.data.UrlToCheck, timeout=10).read()
        self.text = htmlText.decode("utf-8")
        self.text = html.unescape(self.text)

    def hasResultChanged(self):
        oldResult1 = self.data.result1
        oldResult2 = self.data.result2
        self.setMutableData()
        print(self.data.resultToString())
        if self.data.result1 > oldResult1 or self.data.result2 > oldResult2:
            # the goal is disallowed by VAR if the current is less than the prior result
            return True
        else:
            return False

    def setAll(self):
        self.setImmutableData()
        self.setMutableData()
        self.setStartTime()

    def setMutableData(self, possibleScheduleChanges: bool = False):
        resultIndex = self.text.find('class="css-bw7eig-topRow"')
        result = self.text[
                 resultIndex + len('class="css-bw7eig-topRow>"'): resultIndex + self.text[resultIndex:-1].find(
                     "</span>")]
        self.data.result1 = result[0:result.find("-") - 1]
        self.data.result2 = result[result.find("-") + 2::]
        minIndex = self.text.find('class="css-lv1jm0-bottomRow"')
        self.data.minGame = self.text[
                            minIndex + len('class="css-lv1jm0-bottomRow">'): self.text[minIndex:-1].find(
                                "</span>") + minIndex]
        if possibleScheduleChanges:
            self.setStartTime()

    def setImmutableData(self):
        team1Index = self.text.find('class="css-er0nau-TeamName e3q4wbq4"')
        self.data.team1 = self.text[team1Index + len('class="css-er0nau-TeamName e3q4wbq4"><span>'):self.text[
                                                                                                          team1Index:-1].find(
            "</span>") + team1Index]
        team2Index = self.text.find('class="css-11064rk-TeamMarkup-applyHover e3q4wbq5"><div '
                                          'style="width:50px;height:50px;background-color:transparent"></div><span '
                                          'class="css-er0nau-TeamName e3q4wbq4"><span>')
        self.data.team2 = self.text[team2Index + len('class="css-11064rk-TeamMarkup-applyHover e3q4wbq5"><div '
                                                           'style="width:50px;height:50px;background-color:transparent'
                                                           '"></div><span class="css-er0nau-TeamName '
                                                           'e3q4wbq4"><span>'):self.text[team2Index:-1].find(
            "</span>") + team2Index]

    def setStartTime(self):
        oldStartTime = self.data.startTime
        startTimeIndex = self.text.find('<time')
        dateScript = self.text[startTimeIndex:-1]
        matchDay = dateScript[dateScript.find("dateTime=") + len("datetime='"): dateScript.find(":") - 3].replace("-",
                                                                                                                  "")
        dateScript = dateScript[dateScript.find("</span>") + len("</span>")::]
        startTime = dateScript[dateScript.find("<span>") + len("<span> "): dateScript.find("</span>")].replace(":", "")
        self.data.startTime = int(matchDay + startTime)
        self.data.estimatedEndOfHalfTime = int(sumTwoTimes(matchDay + startTime, "0100"))
        if oldStartTime != self.data.startTime and self.data.choice is not None:
            if self.data.choice.value == 0:
                self.data.waitUntil = self.data.startTime
            elif self.data.choice.value == -1:
                before = minusTwoTimes(str(oldStartTime), str(self.data.waitUntil)[8::])[8::]
                self.data.waitUntil = minusTwoTimes(str(self.data.startTime), before)


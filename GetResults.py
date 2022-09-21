import time
from urllib.request import urlopen
import DataFile
from selenium import webdriver


class GetResults:
    def __init__(self, url1: list[DataFile.DataFile()]):
        self.driver = None
        self.url1 = url1
        for urlIndex in range(len(url1)):
            self.setInfoWithDecode(self.url1[urlIndex])
            print(self.url1[urlIndex].resultToString())
        print("------------")

    def updateResults(self):
        for url in self.url1:
            if url.minGame == "Full-Time":
                continue
            elif url.minGame == "Half-Time":
                if url.startOfHalfTime != 0 :
                    if (time.time() - url.startOfHalfTime) > 59:
                        self.setInfoWithDecode(url)
                    else:
                        continue
                else:
                    url.startOfHalfTime == time.time()
            elif url.minGame == "Today":
                startTime = time.strftime("%d")+url.result1[0:2] + url.result2[2::]
                print(startTime)
                print(int(time.strftime("%d%H%M")))
                if int(time.strftime("%d%H%M")) > int(startTime):
                    self.setInfoWithDecode(url)
                else :
                    continue
            elif url.minGame == "Tommoroow":
                startTime = str(int(time.strftime("%d"))+1) + url.result1[0:2] + url.result2[2::]
                print(startTime)
                print(int(time.strftime("%d%H%M")))
                if int(time.strftime("%d%H%M")) > int(startTime):
                    self.setInfoWithDecode(url)
                else :
                    continue
            elif  url.minGame == "Cancelled":
                continue

            oldResult1 = url.result1
            oldResult2 = url.result2
            self.setInfoWithDecode(url)
            print(url.resultToString())
            if url.result1 != oldResult1 or url.result2 != oldResult2:
                url.isChanged = True
            else:
                url.isChanged = False

    def setInfoWithWebDrievr(self, dataFile: DataFile.DataFile):
        self.driver = webdriver.Firefox()
        self.driver.get(dataFile.URlTocheck)
        self.driver.maximize_window()
        result = self.driver.find_element("xpath", "//span[@class='css-bw7eig-topRow']").get_attribute('textContent')
        dataFile.result1 = result[0]
        dataFile.result2 = result[4]
        dataFile.team1 = self.driver.find_element("xpath",
                                                  "//span[@class='css-er0nau-TeamName e3q4wbq4']").get_attribute(
            'textContent')
        dataFile.minGame = self.driver.find_element("xpath", "//span[@class='css-lv1jm0-bottomRow']").get_attribute(
            'textContent')
        dataFile.team2 = self.driver.find_element("xpath",
                                                  "//div[@class='css-11064rk-TeamMarkup-applyHover e3q4wbq5']/span[@class='css-er0nau-TeamName e3q4wbq4']").get_attribute(
            'textContent')
        self.driver.close()

    def setInfoWithDecode(self, dataFile: DataFile.DataFile):
        html = urlopen(dataFile.URlTocheck).read()
        text = html.decode("utf-8")
        resultScript = text.find('class="css-bw7eig-topRow"')
        result = text[
                 resultScript + len('class="css-bw7eig-topRow>"'): resultScript + text[resultScript:-1].find("</span>")]
        dataFile.result1 = result[0:result.find("-") - 1]
        dataFile.result2 = result[result.find("-") + 2::]
        team1ScriptIndex = text.find('class="css-er0nau-TeamName e3q4wbq4"')
        dataFile.team1 = text[team1ScriptIndex + len('class="css-er0nau-TeamName e3q4wbq4"><span>'):text[
                                                                                                    team1ScriptIndex:-1].find(
            "</span>") + team1ScriptIndex]
        team2ScriptIndex = text.find('class="css-11064rk-TeamMarkup-applyHover e3q4wbq5"><div '
                                     'style="width:50px;height:50px;background-color:transparent"></div><span '
                                     'class="css-er0nau-TeamName e3q4wbq4"><span>')
        dataFile.team2 = text[team2ScriptIndex + len('class="css-11064rk-TeamMarkup-applyHover e3q4wbq5"><div '
                                                     'style="width:50px;height:50px;background-color:transparent'
                                                     '"></div><span class="css-er0nau-TeamName '
                                                     'e3q4wbq4"><span>'):text[team2ScriptIndex:-1].find(
            "</span>") + team2ScriptIndex]

        minScriptIndex = text.find('class="css-lv1jm0-bottomRow"')
        dataFile.minGame = text[minScriptIndex + len('class="css-lv1jm0-bottomRow">'): text[minScriptIndex:-1].find(
            "</span>") + minScriptIndex]

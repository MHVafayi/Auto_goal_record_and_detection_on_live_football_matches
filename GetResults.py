import time
from urllib.request import urlopen
import DataFile
from selenium import webdriver


class GetResults:
    def __init__(self, data: DataFile.DataFile()):
        self.data = data
    def updateResults(self):
        oldResult1 = self.data.result1
        oldResult2 = self.data.result2
        self.setInfoWithDecode()
        print(self.data.resultToString())
        if self.data.result1 != oldResult1 or self.data.result2 != oldResult2:
            return True
        else:
            return False

    def setInfoWithWebDrievr(self, data: DataFile.DataFile):
        # it doesn't work because "self.driver" is undefined i just wanted to have this piece of code so its reminded here

        self.driver = webdriver.Firefox()
        self.driver.get(data.URlTocheck)
        self.driver.maximize_window()
        result = self.driver.find_element("xpath", "//span[@class='css-bw7eig-topRow']").get_attribute('textContent')
        data.result1 = result[0]
        data.result2 = result[4]
        data.team1 = self.driver.find_element("xpath",
                                                  "//span[@class='css-er0nau-TeamName e3q4wbq4']").get_attribute(
            'textContent')
        data.minGame = self.driver.find_element("xpath", "//span[@class='css-lv1jm0-bottomRow']").get_attribute(
            'textContent')
        data.team2 = self.driver.find_element("xpath",
                                                  "//div[@class='css-11064rk-TeamMarkup-applyHover e3q4wbq5']/span[@class='css-er0nau-TeamName e3q4wbq4']").get_attribute(
            'textContent')
        self.driver.close()

    def setInfoWithDecode(self):
        html = urlopen(self.data.URlTocheck).read()
        text = html.decode("utf-8")
        resultScript = text.find('class="css-bw7eig-topRow"')
        result = text[
                 resultScript + len('class="css-bw7eig-topRow>"'): resultScript + text[resultScript:-1].find("</span>")]
        self.data.result1 = result[0:result.find("-") - 1]
        self.data.result2 = result[result.find("-") + 2::]
        team1ScriptIndex = text.find('class="css-er0nau-TeamName e3q4wbq4"')
        self.data.team1 = text[team1ScriptIndex + len('class="css-er0nau-TeamName e3q4wbq4"><span>'):text[
                                                                                                    team1ScriptIndex:-1].find(
            "</span>") + team1ScriptIndex]
        team2ScriptIndex = text.find('class="css-11064rk-TeamMarkup-applyHover e3q4wbq5"><div '
                                     'style="width:50px;height:50px;background-color:transparent"></div><span '
                                     'class="css-er0nau-TeamName e3q4wbq4"><span>')
        self.data.team2 = text[team2ScriptIndex + len('class="css-11064rk-TeamMarkup-applyHover e3q4wbq5"><div '
                                                     'style="width:50px;height:50px;background-color:transparent'
                                                     '"></div><span class="css-er0nau-TeamName '
                                                     'e3q4wbq4"><span>'):text[team2ScriptIndex:-1].find(
            "</span>") + team2ScriptIndex]

        minScriptIndex = text.find('class="css-lv1jm0-bottomRow"')
        self.data.minGame = text[minScriptIndex + len('class="css-lv1jm0-bottomRow">'): text[minScriptIndex:-1].find(
            "</span>") + minScriptIndex]

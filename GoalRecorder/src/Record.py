from time import time, sleep
from GoalRecorder.src import DataFile
import cv2
import numpy as np
import pyautogui
from selenium import webdriver


def sumOfTwoSeconds(num1: int, num2: int):
    result = num1 + num2
    return (int(result / 60) * 100) + (result % 60)


class Record:
    def __init__(self, dataFile: DataFile.DataFile, timeLimitSec: int, delay: int = 0, rewindTimeSec: int = 30, FirefoxProfle: str = ""):
        self.profile = FirefoxProfle
        self.startTime = time()
        self.driver = None
        self.dataFile = dataFile
        self.timeLimit = timeLimitSec
        self.timeLen = sumOfTwoSeconds(delay, rewindTimeSec)

    def record(self):
        if self.dataFile.source == "wait":
            print("No url is given")
            return
        self.__createScreen()
        output = self.dataFile.getFileName()+ ".avi"
        img = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        # get info from img
        height, width, channels = img.shape
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output, fourcc, 13.0, (width, height))
        print("Recording...\nName: " + output)
        startTime = time()
        while time() - startTime < self.timeLimit:
            try:
                img = pyautogui.screenshot()
                image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                out.write(image)
                StopIteration(0.5)
            except KeyboardInterrupt:
                pass

        print("finished")
        out.release()
        cv2.destroyAllWindows()
        self.driver.close()

    def __createScreen(self):
        if self.profile != "":
            profile = webdriver.FirefoxProfile(self.profile)
            self.driver = webdriver.Firefox(firefox_profile=profile)
        else:
            self.driver = webdriver.Firefox()
        self.driver.get(self.dataFile.UrlToPlay)
        self.driver.maximize_window()
        sleep(5)
        self.__screenWork()

    def __screenWork(self):
        def __getLabelOfXOffset(pixel: int):
            action.move_to_element_with_offset(ball, pixel, 0).perform()
            sleep(0.3)
            rewindTime = str(label.get_attribute('innerHTML'))
            rewindTime = rewindTime.replace(":", "")
            return int(rewindTime)

        if self.dataFile.source == "telewebion.com":
            try:
                playButton = self.driver.find_element("xpath", "//button[@class='vjs-big-play-button']")
                playButton.click()
            except:
                try:
                    sleep(2)
                    playButton = self.driver.find_element("xpath", "//button[@class='vjs-big-play-button']")
                    playButton.click()
                except:
                    triesNum = 0
                    while triesNum <= 4:
                        try:
                            fullScreenInOldTheme = self.driver.find_element("xpath",
                                                                            "//button[@aria-label='Full Screen']")
                            self.telewebionOldTheme()
                            return
                        except:
                            self.driver.refresh()
                            sleep(5)
                        try:
                            playButton = self.driver.find_element("xpath", "//button[@class='vjs-big-play-button']")
                            playButton.click()
                            triesNum = 0
                            break
                        except:
                            triesNum += 1
                    if triesNum == 5:
                        raise Exception("the web page doesn't load")
            action = webdriver.ActionChains(self.driver)
            fullScreen = self.driver.find_element("xpath",
                                                  "//button[@class='vjs-fullscreen-control vjs-control vjs-button']")
            ball = self.driver.find_element("xpath", "//div[@class='vjs-play-progress vjs-slider-bar']")
            label = self.driver.find_element("xpath",
                                             "/html/body/app-root/div/div/main/div[1]/app-channel/div[2]/div[1]/div[1]/div/div[1]/app-videojs-player/div/div/div[4]/div[2]/div[1]/div/div[2]/div")


            scrollerWidth = ball.size['width'] / 2
            lowerBound = __getLabelOfXOffset(-int(scrollerWidth))
            if lowerBound < 0:
                lowerBound *= -1
            endTime = time()
            self.timeLen = sumOfTwoSeconds(self.timeLen, int(endTime - self.startTime))
            if self.timeLen > lowerBound:
                rewindPixels = -scrollerWidth
            else:
                try:
                    rewindPixels = (((2 * -scrollerWidth) / lowerBound) * self.timeLen) + scrollerWidth
                except ZeroDivisionError:
                    rewindPixels = scrollerWidth
            action.drag_and_drop_by_offset(ball, rewindPixels, 0).perform()
            sleep(1)
            action.click(fullScreen).perform()

        elif self.dataFile.source == "amzfootball.com":
            self.driver.execute_script("window.scrollTo(0,400)")

        else:
            elementsNum = 0
            action = webdriver.ActionChains(self.driver)
            if self.dataFile.resumeXPath.strip() != "":
                elementsNum += 1
                resume = self.driver.find_element("xpath", self.dataFile.resumeXPath)
                try:
                    action.move_to_element(resume).click(resume).perform()
                except:
                    try:
                        sleep(2)
                        resume = self.driver.find_element("xpath", self.dataFile.resumeXPath)
                        action.move_to_element(resume).click(resume).perform()
                    except:
                        tries = 0
                        while tries <= 2:
                            if elementsNum == 1:
                                self.driver.refresh()
                                sleep(5)
                            try:
                                sleep(1)
                                resume = self.driver.find_element("xpath", self.dataFile.resumeXPath)
                                action.move_to_element(resume).click(resume).perform()
                                tries = 0
                                break
                            except:
                                tries += 1
                        if tries == 3:
                            raise Exception("couldn't find Resume Button")

            if self.dataFile.progressBarXPath != "" and self.dataFile.timeLabelXPath != "":
                elementsNum += 1
                try:
                    ball = self.driver.find_element("xpath", self.dataFile.progressBarXPath)
                except:
                    try:
                        sleep(2)
                        ball = self.driver.find_element("xpath", self.dataFile.progressBarXPath)
                    except:
                        tries = 0
                        while tries < 2:
                            if elementsNum == 1:
                                self.driver.refresh()
                                sleep(5)
                            try:
                                sleep(1)
                                ball = self.driver.find_element("xpath", self.dataFile.progressBarXPath)
                                tries = 0
                                break
                            except:
                                tries += 1
                        if tries == 3:
                            raise Exception("couldn't find Progress-Bar")
                label = self.driver.find_element("xpath", self.dataFile.timeLabelXPath)
                scrollerWidth = ball.size['width'] / 2
                lowerBound = __getLabelOfXOffset(-int(scrollerWidth))
                if lowerBound < 0:
                    lowerBound *= -1
                endTime = time()
                self.timeLen = sumOfTwoSeconds(self.timeLen, int(endTime - self.startTime))
                if self.timeLen > lowerBound:
                    rewindPixels = -scrollerWidth
                else:
                    try:
                        rewindPixels = (((2 * -scrollerWidth) / lowerBound) * self.timeLen) + scrollerWidth
                    except ZeroDivisionError:
                        rewindPixels = scrollerWidth
                action.drag_and_drop_by_offset(ball, rewindPixels, 0).perform()

            if self.dataFile.fullScreenXPath.strip() != "":
                elementsNum += 1
                try:
                    fullScreen = self.driver.find_element("xpath", self.dataFile.fullScreenXPath)
                    action.move_to_element(fullScreen).click(fullScreen).perform()
                except:
                    try:
                        sleep(2)
                        fullScreen = self.driver.find_element("xpath", self.dataFile.fullScreenXPath)
                        action.move_to_element(fullScreen).click(fullScreen).perform()
                    except:
                        tries = 0
                        while tries <= 2:
                            if elementsNum == 1:
                                self.driver.refresh()
                                sleep(5)
                            try:
                                sleep(1)
                                fullScreen = self.driver.find_element("xpath", self.dataFile.fullScreenXPath)
                                action.move_to_element(fullScreen).click(fullScreen).perform()
                                tries = 0
                                break
                            except:
                                tries += 1
                        if tries == 3:
                            raise Exception("couldn't find Full-Screen Button")

    def telewebionOldTheme(self):
        try:
            action = webdriver.ActionChains(self.driver)
            fullScreen = self.driver.find_element("xpath", "//button[@aria-label='Full Screen']")
            ball = self.driver.find_element("xpath", "//div[@class='rmp-loaded']")
            rewindInt = 0
            rewindPixels = 0
            endTime = time()
            self.timeLen += endTime - self.startTime
            while rewindInt <= self.timeLen:
                rewindPixels -= 2
                action.move_to_element_with_offset(ball, 430 + rewindPixels, 0).perform()
                rewindTime = self.driver.find_element("xpath",
                                                      "/html/body/app-root/div/div/main/div[1]/app-channel/div[2]/div[1]/div[1]/div/div[1]/app-radiant-player/div/div/div/div[4]/div[2]/div/div[4]/span").get_attribute(
                    'innerHTML')
                rewindTime = rewindTime[::-1]
                timeMark = rewindTime.find(":")
                rewindTime = rewindTime[0:2] + rewindTime[timeMark + 1: timeMark + 3]
                rewindTime = rewindTime[::-1]
                rewindInt = int(rewindTime)
        except:
            sleep(10)
            self.telewebionOldTheme()
            return
        action.drag_and_drop_by_offset(ball, 430 + rewindPixels, 0).perform()
        action.move_to_element(fullScreen).click(fullScreen).perform()


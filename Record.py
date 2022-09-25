import time

import selenium.webdriver.firefox.webdriver

import DataFile
import cv2
import numpy as np
import pyautogui
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox import firefox_profile
from selenium.webdriver.common.keys import Keys

class Record:
    def __init__(self, dataFile: DataFile.DataFile, timeLimitSec: int, delay: int = 0, rewindTimeSec : int= 50):
        self.driver = None
        self.delay = delay
        self.dataFile = dataFile
        self.timeLimit = timeLimitSec
        self.timeLen = rewindTimeSec

    def record(self):
        # webbrowser.open(self.url.getUrl())  # Go to example.com

        # maximize screen
        self.__createScreen()
        output = self.dataFile.getFileName() + ".avi"
        img = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        # get info from img
        height, width, channels = img.shape
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output, fourcc, 13.0, (width, height))
        print("Recording...\nFilename: "+output)
        startTime = time.time()
        while (time.time() - startTime < self.timeLimit):
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
        profile = webdriver.FirefoxProfile("C:\\Users\\98919\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\gkph3dtd.default-release")
        self.driver = webdriver.Firefox(firefox_profile=profile)
        self.driver.get(self.dataFile.URLToPlay)
        self.driver.maximize_window()
        time.sleep(5)
        self.__screenWork()

    def __screenWork(self):
        if self.dataFile.source == "telewebion":
            try:
                try:
                    playButton = self.driver.find_element("xpath", "//button[@class='vjs-big-play-button']")
                    playButton.click()
                except:
                    try:
                        time.sleep(2)
                        playButton = self.driver.find_element("xpath", "//button[@class='vjs-big-play-button']")
                        playButton.click()
                    except:
                        triesNum = 0
                        while triesNum <= 2:
                            self.driver.refresh()
                            time.sleep(2)
                            try:
                                playButton = self.driver.find_element("xpath", "//button[@class='vjs-big-play-button']")
                                playButton.click()
                                triesNum = 0
                                break
                            except :
                                triesNum+=1
                        if triesNum ==2:
                            print("the web page doesn't load")
                            return
                action = webdriver.ActionChains(self.driver)
                fullScreen = self.driver.find_element("xpath", "//button[@class='vjs-fullscreen-control vjs-control vjs-button']")
                ball = self.driver.find_element("xpath", "//div[@class='vjs-play-progress vjs-slider-bar']")
                #try:
                rewindPixels = 0
                rewindInt = 0
                while rewindInt <= self.timeLen:
                    rewindPixels -= 2
                    action.move_to_element_with_offset(ball ,430 + rewindPixels , 0).perform()
                    rewindTime = self.driver.find_element("xpath",
                                                          "/html/body/app-root/div/div/main/div[1]/app-channel/div[2]/div[1]/div[1]/div/div[1]/app-videojs-player/div/div/div[4]/div[2]/div[1]/div/div[2]/div").get_attribute(
                        'innerHTML')
                    time.sleep(0.2)
                    rewindTime = rewindTime[::-1]
                    timeMark = rewindTime.find(":")
                    rewindTime = rewindTime[0:2] +rewindTime[timeMark + 1: timeMark + 3]
                    rewindTime = rewindTime[::-1]
                    print(rewindTime)
                    rewindInt = int(rewindTime)
                action.drag_and_drop_by_offset(ball ,430 + rewindPixels , 0).perform()
                time.sleep(1)
                action.click(fullScreen).perform()
                self.__makeSureVideoIsntStopped()
            except:
                action = webdriver.ActionChains(self.driver)
                fullScreen = self.driver.find_element("xpath", "//button[@aria-label='Full Screen']")
                ball = self.driver.find_element("xpath", "//div[@class='rmp-loaded']")
                rewindInt =0
                rewindPixels =0
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
                    print(rewindTime)
                    rewindInt = int(rewindTime)
                action.drag_and_drop_by_offset(ball, 430+ rewindPixels, 0).perform()
                action.move_to_element(fullScreen).click(fullScreen).perform()




        elif self.dataFile.source == "aparat":

            screen = self.driver.find_element("xpath", "//div[@class='center-bar']")
            # # screen.click()
            action = webdriver.ActionChains(self.driver)
            action.click(screen)
            fullScreen = self.driver.find_element("xpath", "//button[@aria-label='تمام صفحه F']")
            try:
                action.click(screen).perform()
                fullScreen.click()
            except:
                action.click(screen).perform()
                fullScreen.click()
            self.__makeSureVideoIsntStopped()


        elif self.dataFile.source == "anten":
                fullScreen = self.driver.find_element("xpath", "//button[@class='vjs-fullscreen-control vjs-control vjs-button']")
                action = webdriver.ActionChains(self.driver)
                action.move_to_element(fullScreen).perform()
                time.sleep(1)
                action.click(fullScreen).perform()




        elif self.dataFile.source == "unknown and Full-Screen button is unstable":
            tries = 0
            try:
                screen = self.driver.find_element("xpath",
                                                  "//" + self.dataFile.videoBoxTag + "[@" + self.dataFile.videoBoxAttribute + "=" + self.dataFile.videoBoxValue + "]")
                # # screen.click()
                action = webdriver.ActionChains(self.driver)
                action.click(screen)
            except:
                raise Exception("couldn't find videoBox with this information")
            fullScreen = self.driver.find_element("xpath", "xpath",
                                                  "//" + self.dataFile.tag + "[@" + self.dataFile.attribute + "=" +self.dataFile.value+ "]")
            try:
                action.click(screen)
                fullScreen.click()
            except:
                try:
                    time.sleep(10)
                    action.click(screen)
                    fullScreen.click()
                    action.click(screen)
                except:
                    if (tries <= 3):
                        print("your connection is bad :(")
                        tries += 1
                        self.driver.refresh()
                        self.__screenWork()
                    else:
                        raise Exception("couldn't find Full-Screen Button")
            # try:
            #     # play = self.driver.find_element("xpath", "//button[@aria-label='Play']")
            #     screen.click()
            # except:
            #     # the video isnt stoped
            #     pass

        elif self.dataFile.source == "amzfootball":

            self.driver.execute_script("window.scrollTo(0,400)")


        else:

            tries = 0
            fullScreen = self.driver.find_element("xpath", "//" + self.dataFile.tag + "[@" + self.dataFile.attribute + "=" +self.dataFile.value+ "]")
            try:
                fullScreen.click()
            except:
                try:
                    if tries <= 2:
                        time.sleep(10)
                        fullScreen.click()
                    else:
                        raise Exception("couldn't find Full-Screen Button")
                except:
                    if tries <= 2:
                        print("your connection is bad :(")
                        tries += 1
                        self.driver.refresh()
                        self.__screenWork()
                    else:
                        raise Exception("couldn't find Full-Screen Button")
            # try:
            #     # play = self.driver.find_element("xpath", "//button[@aria-label='Play']")
            #     screen.click()
            # except:
            #     # the video isnt stoped
            #     pass

    def __makeSureVideoIsntStopped(self):
        try:
            if self.dataFile.source == "telewebion":
                MainPLay = self.driver.find_element("xpath", "//button[@class='vjs-big-play-button']")
                MainPLay.click()
            elif self.dataFile.source == "aparat":
                play = self.driver.find_element("xpath", "//button[@aria-label='پخش K']")
                play.click()
            elif self.dataFile.source =="anten":
                play = self.driver.find_element("xpath", "//span[@class='vjs-icon-placeholder']")
                play.click()
        except:
            # the video isnt stoped
            pass

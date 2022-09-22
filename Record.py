import time

import selenium.webdriver.firefox.webdriver

import DataFile
import cv2
import numpy as np
import pyautogui
from selenium import webdriver
from selenium.webdriver.firefox import firefox_profile

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import by


class Record:
    def __init__(self, dataFile: DataFile.DataFile, timeLimit: int, delay: int):
        self.driver = None
        self.delay = delay
        self.dataFile = dataFile
        self.timeLimit = timeLimit


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
        self.__screenWork(-7 - (self.delay / 9))

    def __screenWork(self, pixels: int = -7):
        if self.dataFile.source == "telewebion":
            try:
                try:
                    playButton = self.driver.find_element("xpath", "//button[@class='vjs-big-play-button']")
                    playButton.click()
                except:
                    time.sleep(2)
                    playButton = self.driver.find_element("xpath", "//button[@class='vjs-big-play-button']")
                    playButton.click()
                action = webdriver.ActionChains(self.driver)
                fullScreen = self.driver.find_element("xpath", "//button[@class='vjs-fullscreen-control vjs-control vjs-button']")
                ball = self.driver.find_element("xpath", "//div[@class='vjs-play-progress vjs-slider-bar']")
                #try:
                action.drag_and_drop_by_offset(ball ,405 + pixels , 0).perform()
                time.sleep(1)
                action.click(fullScreen).perform()
                # except:
                #     # try:
                #     #     time.sleep(6)
                #     #     skipAd = self.driver.find_element("xpath", "//button[@aria-label='Skip Ad']")
                #     #     skipAd.click()
                #     #     self.__screenWork(-9)
                #     # except:
                #     #      print("your connection is bad :(")
                #     #      self.driver.refresh()
                #     #      time.sleep(10)
                #     #      self.__makeSureVideoIsntStopped()
                #     time.sleep(10)
                #     self.__screenWork(-8)
                self.__makeSureVideoIsntStopped()
            except:
                try:
                    screen = self.driver.find_element("xpath", "//div[@class='rmp-ad-container']")
                except:
                    self.__makeSureVideoIsntStopped()
                    time.sleep(1)
                    screen = self.driver.find_element("xpath", "//div[@class='rmp-ad-container']")

                    # # screen.click()
                action = webdriver.ActionChains(self.driver)
                action.click(screen)
                fullScreen = self.driver.find_element("xpath", "//button[@aria-label='Full Screen']")
                ball = self.driver.find_element("xpath", "//div[@class='rmp-handle rmp-color-bg-button']")
                try:
                    action.drag_and_drop_by_offset(ball, pixels, 0).perform()
                    action.click(screen)
                    fullScreen.click()
                except:
                    # try:
                    #     time.sleep(6)
                    #     skipAd = self.driver.find_element("xpath", "//button[@aria-label='Skip Ad']")
                    #     skipAd.click()
                    #     self.__screenWork(-9)
                    # except:
                    #      print("your connection is bad :(")
                    #      self.driver.refresh()
                    #      time.sleep(10)
                    #      self.__makeSureVideoIsntStopped()
                    time.sleep(10)
                    self.__screenWork(-8)




        elif self.dataFile.source == "aparat":

            screen = self.driver.find_element("xpath", "//div[@class='center-bar']")
            # # screen.click()
            action = webdriver.ActionChains(self.driver)
            action.click(screen)
            fullScreen = self.driver.find_element("xpath", "//button[@aria-label='تمام صفحه F']")
            try:
                action.click(screen)
                fullScreen.click()
            except:
                self.driver.refresh()
                self.__screenWork()
            self.__makeSureVideoIsntStopped()


        elif self.dataFile.source == "anten":
            try:
                screen = self.driver.find_element("xpath", "//div[@aria-label='پخش کننده ویدیو']")
                # # screen.click()
                action = webdriver.ActionChains(self.driver)
                action.click(screen)
                fullScreen = self.driver.find_element("xpath", "//span[@class='vjs-icon-placeholder']")
                try:
                    action.click(screen)
                    fullScreen.click()
                except:
                    print("your connection is bad :(")
                    self.driver.refresh()
                    self.__screenWork()
                self.__makeSureVideoIsntStopped()
            except:
                enter = self.driver.find_element("xpath", "//button[@class='btn btn-primary btn-player player-overlay--cta mx-auto d-table']")
                enter.click()
                time.sleep(1)



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

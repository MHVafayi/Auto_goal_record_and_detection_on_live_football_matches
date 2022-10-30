from urllib.parse import urlparse
import validators
from GoalRecorder.src.Other import AskMe
from GoalRecorder.src.Control import Control


class UserInterface:
    def __init__(self):
        self.mainMenu()

    def mainMenu(self):
        while True:
            print("Each option's number can be written down")
            print("1- Start 2- Stream Websites 3- Settings 4- Help 5- Exit")
            option = input("what should i do?").strip()
            if option == "1" or option.lower().find("start") != -1:
                self.start()
                break
            elif option == "2" or option.lower().find("stream") != -1:
                self.streamUrls()
                break
            elif option == "3" or option.lower().find("settings") != -1:
                self.settings()
                break
            elif option == "4" or option.lower().find("help") != -1:
                while True:
                    print("--------")
                    print("1- what is the purpose of this program? 2- how can i start it? 3- what is the purpose of stream websites? 4- what is importance level? 5- back")
                    option = input().strip().lower()
                    if option == "1" or option.find("purpose") != -1:
                        print("--------")
                        print("this program's major purpose is to check and record football goals in games.")
                    elif option == "2" or option.find("start") != -1:
                        print("--------")
                        print("it needs at least two Urls to start an Url from a live stream to record goal if it saw "
                              "any changes in the score\nand another Url for reviewing the results of live matches "
                              "from a website called Fotmob.\nthere are two ways to input Urls:\n1-enter them one by "
                              "one while the program is running however you should enter them again if it stopped for "
                              "whatever reason.\n2- to solve the issue above you can write them in input.txt so if it "
                              "crashed you wouldn't lose them.")
                    elif option == "3" or option.find("stream") != -1:
                        print("--------")
                        print("there are a lot of live stream websites that i can't handle all of them in my code so\n"
                              "in live stream websites you can add, edit, remove them by your wish Therefore when\n"
                              "you use a website if the program finds it in Stream Websites it clicks the buttons\n"
                              "that you fill out to access website according to your preferences.\n"
                              "also its good to mention that if a website allows you to rewind video you can fully record\n"
                              "goals by entering a XPath of Time Label which shows how many minutes the video rewound and a \n"
                              "Progress Bar.")
                    elif option == "4" or option.find("importance") != -1:
                        print("--------")
                        print("the primary purpose if this is to give some live streaming websites priority status\n"
                              "which instructs the program to check and record goals from those websites first when\n"
                              "two teams in two separate matches score at the same time.\n"
                              "my opinion: because rewinding video could compensate the delay, i prefer rate websites\n"
                              "that allows you to go back in time lower than those that don't however this relies on\n"
                              "how many minutes you can rewind.\n"
                              "also its good to mention that the level of websites that weren't in Stream Websites\n"
                              "would consider as zero and also when a website is added its level is one and it can\n"
                              "be changed in edit by your wish.")
                    elif option == "5" or option.find("back") != -1:
                        print("--------")
                        break
            elif option == "5" or option.lower().find("exit") != -1:
                raise SystemExit(0)

    def settings(self):
        while True:
            print("-------------")
            try:
                profile = open("GoalRecorder/src/Profile.txt", 'r', encoding="utf-8")
            except:
                profile = open("src/Profile.txt", 'r', encoding="utf-8")
            print(profile.read())
            profile.close()
            print("1- Firefox profile 2- syncDuration 3- videoLen 4- rewindTime 5- back")
            option = input("what should i do? ").strip()
            if option == "1" or option.lower().find("firefox") != -1 or option.lower().find("profile") != -1:
                while True:
                    print("--------")
                    command = input("1- Edit 2- More information 3- Back: ").strip()
                    if command.lower().find("edit") != -1 or command == "1":
                        print("--------")
                        Firefox = input("Enter new Firefox profile path or write 'back': ").strip()
                        if Firefox.lower() != "back":
                            try:
                                profile = open("GoalRecorder/src/Profile.txt", 'r', encoding="utf-8")
                            except:
                                profile = open("src/Profile.txt", 'r', encoding="utf-8")
                            data = ""
                            for line in profile:
                                if line.lower().strip().find("firefoxprofilepath:") != -1:
                                    data += "FirefoxProfilePath: " + Firefox + "\n"
                                else:
                                    data += line
                            profile.close()
                            try:
                                w = open("GoalRecorder/src/Profile.txt", 'w', encoding="utf-8")
                            except:
                                w = open("src/Profile.txt", 'w', encoding="utf-8")
                            w.write(data)
                            w.close()
                            break
                    elif command.lower().find("info") != -1 or command == "2":
                        print("--------")
                        print("If you want to open your profile in Firefox, it saves the path so you "
                              "don't have to enter it each time until the path changes.")
                    elif command.lower().find("back") != -1 or command == "3":
                        break
                    else:
                        print("--------")
                        print("this option is invalid")

            elif option == "2" or option.lower().find("sync") != -1:
                while True:
                    print("--------")
                    command = input("1- Edit 2- More information 3- Back: ").strip()
                    if command.lower().find("edit") != -1 or command == "1":
                        while True:
                            print("--------")
                            sync = input("Enter new value in seconds or write 'back': ").strip()
                            if sync.lower() == "back":
                                break
                            try:
                                sync = int(sync)
                                try:
                                    profile = open("GoalRecorder/src/Profile.txt", 'r', encoding="utf-8")
                                except:
                                    profile = open("src/Profile.txt", 'r', encoding="utf-8")
                                data = ""
                                for line in profile:
                                    if line.lower().strip().find("syncduration:") != -1:
                                        data += "     syncDuration: " + str(sync) +"\n"
                                    else:
                                        data += line
                                profile.close()
                                try:
                                    w = open("GoalRecorder/src/Profile.txt", 'w', encoding="utf-8")
                                except:
                                    w = open("src/Profile.txt", 'w', encoding="utf-8")
                                w.write(data)
                                w.close()
                                break
                            except ValueError:
                                print("--------")
                                print("it should be a number")

                    elif command.strip().lower().find("info") != -1 or command.strip() == "2":
                        print("--------")
                        print("duration, in seconds, for checking results")
                    elif command.strip().lower().find("back") != -1 or command.strip() == "3":
                        break
                    else:
                        print("--------")
                        print("this option is invalid")

            elif option == "3" or option.lower().find("video") != -1:
                while True:
                    print("--------")
                    command = input("1- Edit 2- More information 3- Back: ").strip()
                    if command.lower().find("edit") != -1 or command == "1":
                        while True:
                            print("--------")
                            video = input("Enter new value in seconds or write 'back': ").strip()
                            if video.lower() == "back":
                                break
                            try:
                                video = int(video)
                                try:
                                    profile = open("GoalRecorder/src/Profile.txt", 'r', encoding="utf-8")
                                except:
                                    profile = open("src/Profile.txt", 'r', encoding="utf-8")
                                data = ""
                                for line in profile:
                                    if line.lower().strip().find("videolen:") != -1:
                                        data += "     videoLen: " + str(video) + "\n"
                                    else:
                                        data += line
                                profile.close()
                                try:
                                    w = open("GoalRecorder/src/Profile.txt", 'w', encoding="utf-8")
                                except:
                                    w = open("src/Profile.txt", 'w', encoding="utf-8")
                                w.write(data)
                                w.close()
                                break
                            except ValueError:
                                print("--------")
                                print("it should be a number")

                    elif command.strip().lower().find("info") != -1 or command.strip() == "2":
                        print("--------")
                        print("record duration, in seconds")
                    elif command.strip().lower().find("back") != -1 or command.strip() == "3":
                        break
                    else:
                        print("--------")
                        print("this option is invalid")

            elif option == "4" or option.lower().find("rewind") != -1:
                while True:
                    print("--------")
                    command = input("1- Edit 2- More information 3- Back: ").strip()
                    if command.lower().find("edit") != -1 or command == "1":
                        while True:
                            print("--------")
                            rewind = input("Enter new value in seconds or write 'back': ").strip()
                            if rewind.lower() == "back":
                                break
                            try:
                                rewind = int(rewind)
                                try:
                                   profile = open("GoalRecorder/src/Profile.txt", 'r', encoding="utf-8")
                                except:
                                    profile = open("src/Profile.txt", 'r', encoding="utf-8")
                                data = ""
                                for line in profile:
                                    if line.lower().strip().find("rewindtime:") != -1:
                                        data += "     rewindTime: " + str(rewind) + "\n"
                                        print(data)
                                    else:
                                        data += line
                                profile.close()
                                try:
                                    w = open("GoalRecorder/src/Profile.txt", 'w', encoding="utf-8")
                                except:
                                    w = open("src/Profile.txt", 'w', encoding="utf-8")
                                w.write(data)
                                w.close()
                                break
                            except ValueError:
                                print("--------")
                                print("it should be a number")

                    elif command.strip().lower().find("info") != -1 or command.strip() == "2":
                        print("--------")
                        print("Timespan in seconds to rewind video, just have use in Telewebion urls")
                    elif command.strip().lower().find("back") != -1 or command.strip() == "3":
                        break
                    else:
                        print("--------")
                        print("this option is invalid")
            elif option == "5" or option.lower().find("back") != -1:
                print("-------------")
                self.mainMenu()
                return

    def streamUrls(self):
        while True:
            print("-------------")
            print("1- add 2-show 3- edit 4-remove 5-back")
            option = input("what should i do?").strip()
            # add
            if option == "1" or option.lower().find("add") != -1:
                while True:
                    print("--------")
                    url = input("enter a url from the website that you want or write 'back':\n").strip()
                    if url.lower() == "back":
                        break
                    if validators.url(url):
                        domain = str(urlparse(url).netloc)
                        try:
                            file = open("GoalRecorder/src/StreamWebsites.txt", "r", encoding="utf-8")
                        except:
                            file = open("src/StreamWebsites.txt", "r", encoding="utf-8")
                        founded = False
                        for line in file:
                            if line.strip().find(domain) != -1:
                                founded = True
                                break
                        file.close()
                        if not founded:
                            print("--------")
                            print(
                                "you will be asked to enter XPath of the buttons that you want to click in this website. otherwise you can write 'skip' or '0'")
                            fullScreen = input("Ful screen: ").strip()
                            resume = input("Resume: ").strip()
                            if fullScreen.lower() == "skip" or fullScreen == "0":
                                fullScreen = ""
                            if resume.lower() == "skip" or resume == "0":
                                resume = ""
                            progressBar = input("Progress Bar to rewind live stream: ").strip()
                            label = ""
                            if progressBar.lower() == "skip" or progressBar == "0":
                                progressBar = ""
                            else:
                                while progressBar != "":
                                    if label.lower() == "skip" or label == "0":
                                        print("--------")
                                        print("its required for Progress Bar, so you can't skip it. 1- enter Time label XPath 2- delete Progress Bar XPath")
                                        while True:
                                            command = input().strip()
                                            if command.lower().find("enter") != -1 or command == "1":
                                                label = ""
                                                break
                                            elif command.lower().find("delete") != -1 or command == "2":
                                                progressBar = ""
                                                label = ""
                                                break
                                            else:
                                                print("this option is invalid")
                                    else:
                                        label = input("Time Label to check rewind time: ").strip()
                                        if label.lower() != "skip" and label != "0":
                                            break

                            try:
                                w = open("GoalRecorder/src/StreamWebsites.txt", "a", encoding="utf-8")
                            except:
                                w = open("src/StreamWebsites.txt", "a", encoding="utf-8")
                            w.write(
                                "\n" + domain + ": importance = 1\n      FullScreen: " + fullScreen + "\n      Resume: " + resume +
                                "\n      TimeLabel: " + label + "\n      ProgressBar: " + progressBar)
                            w.close()
                            print("Successfully added")
                            break
                        else:
                            print("--------")
                            print("you have already added this website")
                    else:
                        print("--------")
                        print("the url is invalid")
            # show
            elif option == "2" or option.lower().find("show") != -1:
                try:
                    file = open("GoalRecorder/src/StreamWebsites.txt", "r", encoding="utf-8")
                except:
                    file = open("src/StreamWebsites.txt", "r", encoding="utf-8")
                result = file.read()
                file.close()
                print("--------")
                print(result)
            # edit
            elif option == "3" or option.lower().find("edit") != -1:
                while True:
                    print("--------")
                    url = input("enter a url from the website that you want to edit or write 'back':\n").strip()
                    if url.lower() == "back":
                        break
                    if validators.url(url):
                        try:
                            file = open("GoalRecorder/src/StreamWebsites.txt", "r", encoding="utf-8")
                        except:
                            file = open("src/StreamWebsites.txt", "r", encoding="utf-8")
                        domain = str(urlparse(url).netloc)
                        nowIn = False
                        data = ""
                        founded = False
                        for line in file:
                            if line.strip().find(domain) != -1:
                                nowIn = True
                                founded = True
                                print("do you want to change importance level? (the higher number is in priority):")
                                while True:
                                    a = input().strip().lower()
                                    if a.find("yes") != -1:
                                        while True:
                                            b = input("new value (a number greater than zero): ").strip()
                                            try:
                                                value = int(b)
                                                if value > 0:
                                                    data += line[0:line.find("importance")] +"importance: " + str(value) + "\n"
                                                    break
                                                else:
                                                    print("--------")
                                                    print("it should greater than zero")
                                            except ValueError:
                                                print("--------")
                                                print("you should enter a number")
                                        break
                                    elif a.find("no") != -1:
                                        data += line
                                        break
                                    else:
                                        print("--------")
                                        print("Enter yes or no")
                            elif nowIn:
                                if line.find("FullScreen:") != -1:
                                    while True:
                                        x = input("do you want to edit FullScreen XPath? ").strip().lower()
                                        if x == "yes":
                                            XPath = input("XPath: ").strip()
                                            data += "     FullScreen: " + XPath + "\n"
                                            break
                                        elif x == "no":
                                            data += line
                                            break
                                        else:
                                            print("--------")
                                            print("Enter yes or no")

                                elif line.find("Resume:") != -1:
                                    while True:
                                        x = input("do you want to edit Resume XPath? ").strip().lower()
                                        if x == "yes":
                                            XPath = input("XPath: ").strip()
                                            data += "     Resume: " + XPath + "\n"
                                            break
                                        elif x == "no":
                                            data += line
                                            break
                                        else:
                                            print("--------")
                                            print("Enter yes or no")

                                elif line.find("TimeLabel:") != -1:
                                    while True:
                                        x = input("do you want to edit Time label XPath? ").strip().lower()
                                        if x == "yes":
                                            XPath = input("XPath: ").strip()
                                            if XPath == "":
                                                print("--------")
                                                print("be careful Time label and Progress Bar both are required for rewinding live "
                                                      "streams so if you remove one of them this feature doesn't work")
                                                print("--------")
                                            data += "     TimeLabel: " + XPath + "\n"
                                            break
                                        elif x == "no":
                                            data += line
                                            break
                                        else:
                                            print("--------")
                                            print("Enter yes or no")

                                elif line.find("ProgressBar:") != -1:
                                    while True:
                                        x = input("do you want to edit Progress Bar XPath? ").strip().lower()
                                        if x == "yes":
                                            XPath = input("XPath: ").strip()
                                            if XPath == "":
                                                print("--------")
                                                print("be careful Time label and Progress Bar both are required for rewinding live "
                                                      "streams so if you remove one of them this feature doesn't work")
                                            data += "     ProgressBar: " + XPath + "\n"
                                            break
                                        elif x == "no":
                                            data += line
                                            break

                                else:
                                    nowIn = False
                            else:
                                data += line
                        if founded:
                            file.close()
                            try:
                                write = open("GoalRecorder/src/StreamWebsites.txt", "w", encoding="utf-8")
                            except:
                                write = open("src/StreamWebsites.txt", "w", encoding="utf-8")
                            write.write(data)
                            write.close()
                            print("Successfully edited")
                            break
                        else:
                            print("--------")
                            print("Nothing found")
                    else:
                        print("--------")
                        print("the url is invalid")
            elif option == "4" or option.lower().find("remove") != -1:
                while True:
                    print("--------")
                    url = input("enter a url from the website that you want to edit or write 'back':\n").strip()
                    if url.lower() == "back":
                        break
                    if validators.url(url):
                        try:
                            file = open("GoalRecorder/src/StreamWebsites.txt", "r", encoding="utf-8")
                        except:
                            file = open("src/StreamWebsites.txt", "r", encoding="utf-8")
                        domain = str(urlparse(url).netloc)
                        nowIn = False
                        data = ""
                        founded = False
                        for line in file:
                            if line.strip().find(domain) != -1:
                                nowIn = True
                                founded = True
                            elif nowIn:
                                if line.find(".") != -1:
                                    nowIn = False
                                    data += line
                            else:
                                data += line
                        if founded:
                            file.close()
                            try:
                                write = open("GoalRecorder/src/StreamWebsites.txt", "w", encoding="utf-8")
                            except:
                                write = open("src/StreamWebsites.txt", "w", encoding="utf-8")
                            write.write(data)
                            write.close()
                            print("Successfully removed")
                            break
                        else:
                            print("--------")
                            print("Nothing found")
                    else:
                        print("--------")
                        print("the url is invalid")
            elif option == "5" or option.lower().find("back") != -1:
                print("-------------")
                self.mainMenu()
                return

    def start(self):
        def checkFotmobUrl(u: str):
            u = u.strip()
            if validators.url(u):
                if u.lower().find("fotmob") != -1:
                    return "Ok"
                else:
                    return "Not Fotmob"
            elif u.lower() == "done":
                return "Done"
            elif u.lower().find("stream urls:") != -1:
                return "Stream"
            else:
                return "Invalid"

        urlsToCheck = []
        urlsToPlay = []

        while True:
            print("-------------")
            print("1- read from input.txt 2- enter now 3- back")
            option = input("What should i do?").strip()
            if option == "1" or option.lower().find("read") != -1:
                try:
                    file = open("GoalRecorder/input.txt", 'r')
                except:
                    file = open("input.txt", 'r')
                    now = ""
                    lineNum = 0
                    for line in file:
                        lineNum += 1
                        line = line.strip()
                        if line.lower().find("fotmob urls:") != -1:
                            now = "Fotmob"
                            continue
                        elif line.lower().find("stream urls:") != -1:
                            now = "Stream"
                            continue
                        elif now == "Fotmob":
                            condition = checkFotmobUrl(line)
                            if condition == "Ok":
                                urlsToCheck.append(line)
                            elif condition == "Not Fotmob":
                                print("--------")
                                raise Exception("the " + line + " in line number " + str(
                                    lineNum) + " in input.txt is not Fotmob, its " + str(urlparse(line).netloc))
                            elif condition == "Stream":
                                now = "Stream"
                            else:
                                print("--------")
                                raise Exception("the " + line + " in line number " + str(lineNum) + " is invalid")
                        elif now == "Stream":
                            if line.lower() == "before":
                                urlsToPlay.append(AskMe.BEFORE_THE_MATCH_STARTS)
                            elif line.lower() == "later":
                                urlsToPlay.append(AskMe.LATER)
                            elif line.lower() == "start":
                                urlsToPlay.append(AskMe.WHEN_THE_MATCH_STARTS)
                            else:
                                if validators.url(line):
                                    urlsToPlay.append(line)
                                else:
                                    print("--------")
                                    raise Exception(
                                        "the " + line + " in line number " + str(lineNum) + " is invalid")
                    file.close()
                    break



            elif option == "2" or option.lower().find("enter") != -1:
                print("--------")
                print(
                    "you must Enter some 'Fotmob' urls to check the results and some live stream urls to record the "
                    "goals, then type 'done' once you have finished.\nalso, "
                    "if you dont have a live stream right now you can choose one of the following options: 1- before (enter before the "
                    "match starts) 2- start(when the match starts) 3- later")
                fotmob = ""
                stream = ""
                while fotmob.lower() != "done":
                    print("--------")
                    while True:
                        fotmob = str(input("Url to check:")).strip()
                        condition = checkFotmobUrl(fotmob)
                        if condition == "Ok":
                            urlsToCheck.append(fotmob)
                            break
                        elif condition == "Not Fotmob":
                            print("--------")
                            print("you must enter a url from one of the football matches in Fotmob website.")
                        elif condition == "Done":
                            break
                        else:
                            print("--------")
                            print("the url is invalid")

                    while fotmob.lower() != "done":
                        stream = str(input("Url to record: ")).strip()
                        if validators.url(stream):
                            urlsToPlay.append(stream)
                            break
                        elif stream.lower().find("before") != -1 or fotmob == "1":
                            urlsToPlay.append(AskMe.BEFORE_THE_MATCH_STARTS)
                            break
                        elif stream.lower().find("later") != -1 or fotmob == "3":
                            urlsToPlay.append(AskMe.LATER)
                            break
                        elif stream.lower().find("start") != -1 or fotmob == "2":
                            urlsToPlay.append(AskMe.WHEN_THE_MATCH_STARTS)
                            break
                        elif stream.lower() == "done":
                            print("--------")
                            print(
                                "you either must enter a live stream url with url above or delete url to check choose one of "
                                "the following options: 1- continue 2-delete")
                            while True:
                                z = input("what should i do ?").strip()
                                if z.lower().find("continue") != -1 or z == "1":
                                    break
                                elif z.lower().find("delete") != -1 or z == "2":
                                    del urlsToCheck[len(urlsToCheck) - 1]
                                    break
                                else:
                                    print("--------")
                                    print("you must write one of the options")
                            if z.lower().find("delete") != -1 or z == "2":
                                break
                        else:
                            print("--------")
                            print("the url is invalid")
                break
            elif option == "3" or option.lower().find("back") != -1:
                print("-------------")
                self.mainMenu()
                return
        print("please wait...")
        Control(UrlForCheckScore=urlsToCheck, UrlForRecord=urlsToPlay).start()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    UserInterface()
    # print("vgvfyer")
    # data = DataFile()
    # data.UrlToPlay = "https://telewebion.com/live/tv3"
    # data.setSource()
    # data.setElementsXPath()
    # profile = getProfile()
    # Record(dataFile=data, timeLimitSec=15, FirefoxProfle= profile , rewindTimeSec=0).record()
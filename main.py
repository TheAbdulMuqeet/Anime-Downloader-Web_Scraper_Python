from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import os

try:
    startingEpisodeNumber = 0
    episodeDownloadable = 0
    endingEpisodeNumber = 0
    episodesToDownload = []
    names_of_episodesToDownload = []
    episodes_not_downloaded = []
    episodes_downloaded = []
    episodes = []
    count = 0
    totalEpisodes = 0
    choice = 0
    tempBool = 0
    all_downloaded = 0
    browser = 0
    _404 = 0

    # Selection of the browser
    while (browser < 1 or browser > 2):
        os.system("cls")
        print("Select the browser")
        browser = int(input("""
            1. Chrome browser
            2. Microsoft Edge
            Selection: """))

    # Selecting download method
    while (not choice >= 1 or not choice <= 3):
        if (tempBool > 0):
            print("==> Please enter the right options")
        print("\nChoose download method:")
        choice = int(input("""
            1. All episodes
            2. Range of episodes
            3. Some episodes
            Selection: """))
        tempBool += 1

    print("\nEnter data required to start the download")
    print("------------------------------------------", end="\n")


    mainLink = input("Enter archive link: ")
    # download_directory = input("Enter download directory (the download directory your browser have): ")
    download_directory = os.path.join(os.path.expandvars("%userprofile%"), "Downloads")


    if choice == 2:
        startingEpisodeNumber = int(input("Enter starting episode number: "))
        endingEpisodeNumber = int(input("Enter ending episode number: "))
        episodeDownloadable = (endingEpisodeNumber - startingEpisodeNumber) + 1
    elif choice == 3:
        print("Enter episode numbers (press 0 to exit)")
        temp = -1
        while (temp != 0):
            temp = int(input("Episode "))
            if (int(temp) and temp != 0):
                episodesToDownload.append(temp)
        episodesToDownload.sort()
        print("Episode(s) ", episodesToDownload, " will be downloaded")
        episodeDownloadable = len(episodesToDownload)

    # Starting the driver
    print("===================================================")
    print("The browser is now starting...")

    # Adding arguments
    if browser == 2:
        options = webdriver.EdgeOptions()
    else:
        options = webdriver.ChromeOptions()

    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Opening the browser
    if browser == 2:
        driver = webdriver.Edge(options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.set_window_position(0, 0, windowHandle='current')
    driver.get(mainLink)
    print("Please wait! Counting the episodes...")
    elements = driver.find_elements(By.XPATH, '//h3/a')

    # counting total episodes
    for element in elements:
        episodes.append(element.get_attribute('href'))
        totalEpisodes += 1

    if choice == 1:
        startingEpisodeNumber = 1
        endingEpisodeNumber = totalEpisodes
        episodeDownloadable = totalEpisodes
    print("Total no. episodes on site : ", totalEpisodes)
    print("No. of episodes to download: ", episodeDownloadable)
    print("===================================================")


    # downloading episodes
    print("Downloads are now started")
    print("==> \tPrompt: if any episode fails to download, re-download it")
    count = 0
    currentEpisodeNumber = startingEpisodeNumber
    for episode in episodes:
        count += 1
        if choice == 1 or choice == 2:
            if (count >= startingEpisodeNumber and count <= endingEpisodeNumber):
                driver.get(episode)
                if (driver.find_element(By.TAG_NAME, 'h3').text == "404! Page Not Found"):
                    print(
                        f"Error: Episode {count} cannot be downloaded because it has been removed from the server")
                    _404 += 1
                    continue
                direct_mirror = driver.find_element(
                    By.CLASS_NAME, 'btn-outline-success')
                driver.get(direct_mirror.get_attribute('href'))

                refresh_mirror = driver.find_element(By.ID, 'checkfile')
                refresh_mirror.click()

                download_direct = driver.find_element(By.CLASS_NAME, 'btn-success')
                driver.get(download_direct.get_attribute('href'))

                names_of_episodesToDownload.append(
                    driver.find_element(By.CLASS_NAME, 'card-header').text)
                download_now = driver.find_element(By.NAME, 'download')
                print(f"Episode {currentEpisodeNumber} is downloading.")
                download_now.click()
                currentEpisodeNumber += 1

        elif choice == 3:
            for i in episodesToDownload:
                if (count == i):
                    if count <= totalEpisodes:
                        currentEpisodeNumber = i
                        driver.get(episode)
                        direct_mirror = driver.find_element(
                            By.CLASS_NAME, 'btn-outline-success')
                        driver.get(direct_mirror.get_attribute('href'))

                        refresh_mirror = driver.find_element(By.ID, 'checkfile')
                        refresh_mirror.click()

                        download_direct = driver.find_element(
                            By.CLASS_NAME, 'btn-success')
                        driver.get(download_direct.get_attribute('href'))

                        names_of_episodesToDownload.append(
                            driver.find_element(By.CLASS_NAME, 'card-header').text)
                        download_now = driver.find_element(By.NAME, 'download')
                        print(f"Episode {currentEpisodeNumber} is downloading.")
                        download_now.click()

                    else:
                        print("Episode ", i , " not found")

    print("\nPlease wait, downloading is in progress...")
    print("Check the browser for download information")
    print("Do not close any tab or the browser")
    dl_wait = True
    while dl_wait:
        dl_wait = False
        for fname in os.listdir(download_directory):
            if fname.endswith('.crdownload'):
                dl_wait = True
    driver.close()
    os.system("cls")
    print("\n==============")
    print("Final result")
    print("=============")
    for episode_name in names_of_episodesToDownload:
        for fname in os.listdir(download_directory):
            if fname == episode_name:
                tempFound = 0
                break
            else:
                tempFound = 1
        if(tempFound):
            episodes_not_downloaded.append(episode_name)
            all_downloaded += 1
        else:
            episodes_downloaded.append(episode_name)
    if all_downloaded == 0:
        print("No errors were encountered.")

    elif not _404 == 0:
        print("No episodes were found on website's server")
    else:
        print("\nRe-download the listed episodes")
        print("-------------------------------")
        for episode_name in episodes_not_downloaded:
            print(f"{episode_name} failed to download")

    print("\nFollowing episodes were succesfully downloaded")
    print("----------------------------------------------")
    for episode_name in episodes_downloaded:
        print(episode_name)
except WebDriverException:
    print("\nBrowser was unexpectedly closed")

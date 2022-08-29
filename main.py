from selenium import webdriver
from selenium.webdriver.common.by import By
import os

startingEpisodeNumber = 0
episodeDownloadable = 0
endingEpisodeNumber = 0
episodesToDownload = []
names_of_episodesToDownload = []
episodes = []
count = 0
totalEpisodes = 0
choice = 0
tempBool = 0
all_downloaded = 0

# Selecting download method
while (not choice >= 1 or not choice <= 3):
    os.system("cls")
    if (tempBool > 0):
        print("==> Please enter the right options")
    print("""
    Choose download method:
        1. All episodes
        2. Range of episodes
        3. Some episodes
        Selection: """, end="")
    choice = int(input(""))
    tempBool += 1

print("\nEnter data required to start the download")
print("------------------------------------------", end="\n")


mainLink = input("Enter archive link: ")
# download_directory = input("Enter download directory (the download directory your browser have): ")
download_directory = os.path.join(
    os.path.expandvars("%userprofile%"), "Downloads")


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
options = webdriver.EdgeOptions()
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Opening the browser
driver = webdriver.Edge(options=options)
driver.set_window_position(0, 0, windowHandle='current')
driver.get(mainLink)
elements = driver.find_elements(By.XPATH, '//h3/a')

# counting total episodes
print("Please wait! Counting the episodes...")
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
for episode in episodes:
    count += 1
    if choice == 1 or choice == 2:
        currentEpisodeNumber = startingEpisodeNumber
        if (count >= startingEpisodeNumber and count <= endingEpisodeNumber):
            driver.get(episode)
            direct_mirror = driver.find_element(
                By.CLASS_NAME, 'btn-outline-success')
            driver.get(direct_mirror.get_attribute('href'))

            refresh_mirror = driver.find_element(By.ID, 'checkfile')
            refresh_mirror.click()

            download_direct = driver.find_element(By.CLASS_NAME, 'btn-success')
            driver.get(download_direct.get_attribute('href'))

            names_of_episodesToDownload.append(driver.find_element(By.CLASS_NAME, 'card-header').text)
            download_now = driver.find_element(By.NAME, 'download')
            download_now.click()
            print(f"Episode {currentEpisodeNumber} is downloading.")

    elif choice == 3:
        for i in episodesToDownload:
            if (count == i):
                if count <= totalEpisodes:
                    driver.get(episode)
                    direct_mirror = driver.find_element(
                        By.CLASS_NAME, 'btn-outline-success')
                    driver.get(direct_mirror.get_attribute('href'))

                    refresh_mirror = driver.find_element(By.ID, 'checkfile')
                    refresh_mirror.click()

                    download_direct = driver.find_element(
                        By.CLASS_NAME, 'btn-success')
                    driver.get(download_direct.get_attribute('href'))

                    download_now = driver.find_element(By.NAME, 'download')
                    download_now.click()
                    print(f"Episode {episodesToDownload[i]} is downloading.")

                else:
                    print("Episode ", episodesToDownload[i], " not found")


dl_wait = True
while dl_wait:
    dl_wait = False
    for fname in os.listdir(download_directory):
        if fname.endswith('.crdownload'):
            dl_wait = True
driver.close()

print("\n=============")
print("Final result")
print("============")
for fname in os.listdir(download_directory):
    for episode_name in names_of_episodesToDownload:
        if fname.startswith(episode_name):
            continue
        else:
            print(f"{episode_name} failed to download")
            all_downloaded += 1

print("")
if all_downloaded == 0:
    print("No errors were encountered")
else:
    print("Re-download the listed episodes")
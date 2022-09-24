import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
download_directory = os.path.join(os.path.expandvars("%userprofile%"), "Downloads")
link_file = "resume_download.txt"

def which_browser():
    # Selection of the browser
    browser = 0
    while (True):
        print("Select the browser")
        try:
            browser = int(input("""
                1. Chrome browser
                2. Microsoft Edge
                Selection: """))
        except ValueError:
            pass

        if(not(browser == 1 or browser == 2)):
            os.system("cls")
            print("Invalid input")
        else:
            return browser

def which_method():
    # Selecting download method
    choice = 0
    print()
    while (True):
        try:
            print("Choose download method:")
            choice = int(input("""
                1. All episodes
                2. Range of episodes
                3. Some episodes
                Selection: """))
        except ValueError:
            pass
        
        if(not(choice == 1 or choice == 2 or choice == 3)):
            os.system("cls")
            print("\nInvalid Choice")
        else:
            return choice

def get_link():
    archive_base = "episodes.animeflix.org.in/archives"
    while(True):
        archive_link = input("Enter archive link: ")
        if(not(archive_base in archive_link)):
            os.system("cls")
            print("Invalid link")
        else:
            return archive_link

def which_episodes(episodeChoice):
    episodes = []
    if(episodeChoice == 2):
        while(True):
            try:
                episodes.append(int(input("Enter starting episode number: ")))
                if(episodes[0] > 0):
                    break
            except ValueError:
                print("Invalid starting episode number")
        while(True):
            try:
                temp = int(input("Enter ending episode number (enter '9876' to select the last episode): "));
                if(temp > 0 and temp > episodes[0]):
                    episodes.append(temp)
                    break
                else:
                    print(f"Ending episode must be greater than starting episode(starting episode: {episodes[0]})")
                    print('----------------------------------------------------------------------------')
            except ValueError:
                print("Invalid ending episode number")
        if temp == 9876:
            pass
        else:
            print(f"{(episodes[1] - episodes[0])+1} episodes will be downloaded (ep {episodes[0]} - ep {episodes[1]})")
    elif(episodeChoice ==3):
        print("Enter episode numbers (enter 0 to exit)")
        temp = -1
        while(True):
            try:
                temp = int(input("Episode "))
                if(temp == 0):
                    break
                episodes.append(temp)
            except ValueError:
                pass
        episodes.sort()
        episodes = list(set(episodes))
        print("Episode(s) ", episodes, " will be downloaded")
    return episodes
            
def are_there_links():
    if link_file in os.listdir():
        with open(link_file, 'r') as resume_process:
            resume_links = resume_process.readlines()
            if resume_links[0].startswith('https://episodes.animeflix.org.in'):
                print("================================================================================================\nBackup file found!")
                resume_choice = input("If you wish to complete/resume your previous incomplete download, enter 'y': ")
                if resume_choice == 'y':
                    return resume_links
    return 0

def driver_process(browser_choice, required_episodes_numbers, method, resume_links = 0):
    if(resume_links == 0):
        mainLink = get_link()
    else:
        mainLink = resume_links[0]

    # Starting the driver
    print("===========================================================================")
    print("The browser is now starting...")

    if browser_choice == 2:
        options = webdriver.EdgeOptions()
    elif browser_choice == 1:
        options = webdriver.ChromeOptions()

    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Opening the browser
    if browser_choice == 2:
        driver = webdriver.Edge(options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.set_window_position(0, 0, windowHandle='current')
    driver.get(mainLink)
    
    links_to_all_episodes = []
    if resume_links == 0:
        # Couting the anchor tags on the page
        print("Please wait! Counting the episodes...")
        elements = driver.find_elements(By.XPATH, '//h3/a')

        # counting total episodes and saving the links
        total_anchor_tags = 0

        with open(link_file, 'w') as writing_episode_links:
            for element in elements:
                total_anchor_tags += 1
                if method == 1:
                    writing_episode_links.write(f"{element.get_attribute('href')}\n")
                    links_to_all_episodes.append(f"{element.get_attribute('href')}\n")
                elif(method == 2):
                    if(total_anchor_tags >= required_episodes_numbers[0] and total_anchor_tags <= required_episodes_numbers[1]):
                        writing_episode_links.write(f"{element.get_attribute('href')}\n")
                        links_to_all_episodes.append(f"{element.get_attribute('href')}\n")
                elif(method == 3):
                    for episode_number in required_episodes_numbers:
                        if(total_anchor_tags == episode_number):
                            writing_episode_links.write(f"{element.get_attribute('href')}\n")            
                            links_to_all_episodes.append(f"{element.get_attribute('href')}\n")
        if method == 1:
            print("No. of episodes to download: ", total_anchor_tags)
        elif method == 2:
            temp = required_episodes_numbers[1]
            start = required_episodes_numbers[0]
            end = len(links_to_all_episodes) + start
            required_episodes_numbers.clear()
            for i in range(start, end):
                required_episodes_numbers.append(i)
            if temp == 9876:
                print(f"{len(required_episodes_numbers)} episodes will be downloaded (ep {required_episodes_numbers[0]} - ep {required_episodes_numbers[-1]})")

        print("Total no. episodes on site : ", total_anchor_tags)
        print("===========================================================================")
    else:
        links_to_all_episodes = resume_links

    # download starts here
    print("Downloads are now starting...")
    print("==> \tPrompt: if any episode fails to download, re-download it")
    episodes_processed = []
    for (episode_link, episode_number)  in zip(links_to_all_episodes, required_episodes_numbers):
        driver.get(episode_link)
        if (driver.find_element(By.TAG_NAME, 'h3').text == "404! Page Not Found"):
            print(f"Error: An episode was not available at website's server")
            continue
        
        direct_mirror = driver.find_element(By.CLASS_NAME, 'btn-outline-success')
        driver.get(direct_mirror.get_attribute('href'))
        refresh_mirror = driver.find_element(By.ID, 'checkfile')
        refresh_mirror.click()

        download_direct = driver.find_element(By.CLASS_NAME, 'btn-success')
        driver.get(download_direct.get_attribute('href'))

        current_episode_name = driver.find_element(By.CLASS_NAME, 'card-header').text
        episodes_processed.append(current_episode_name)
        download_now = driver.find_element(By.NAME, 'download')
        if resume_links == 0:
            print(f"Episode {episode_number} is downloading...")
        else:
            print(f"Episode '{current_episode_name}' is downloading...")

        download_now.click()

    print("\nPlease wait, downloading is in progress...")
    print("Check the browser for download progress")
    print("Do not close the browser or any tab")
    wait()
    driver.close()
    return episodes_processed

def wait():
    sleep(5)
    dl_wait = True
    while dl_wait:
        dl_wait = False
        for fname in os.listdir(download_directory):
            if fname.endswith('.crdownload'):
                dl_wait = True

def main_engine():
    try:
        os.system("cls")
        browser = which_browser()
        resume = are_there_links();

        try:
            downloaded_episodes = []
            if resume == 0:
                choice = which_method()
                print("\nEnter data required to start the download")
                print("------------------------------------------", end="\n")                

                # downloading episodes
                required_episodes = which_episodes(choice)
                downloaded_episodes = driver_process(browser, required_episodes, choice)
            else:
                downloaded_episodes = driver_process(browser, [0, 0], 0, resume_links=resume)

            print("===========================================================================")
            os.system("cls")
            print("\n==============")
            print(" Final result")
            print("==============")

            episode_links_in_file = []
            with open(link_file, 'r') as reading_links:
                episode_links_in_file = reading_links.readlines()
            
            # After Download
            remaining_episode_links = []
            for i in range(len(required_episodes)):
                if downloaded_episodes[i] in os.listdir(download_directory):
                    print(f" OO ==> Episode {required_episodes[i]} successfully downloaded")
                else:
                    remaining_episode_links.append(episode_links_in_file[i])
                    print(f" XX ==> Episode {required_episodes[i]} download failed")

            with open(link_file, 'w') as writing_remaining_links:
                writing_remaining_links.writelines(remaining_episode_links)
                
        except WebDriverException:
            print("\nBrowser was unexpectedly closed (probably due to bad internet connection)\nAll progress was lost. Please restart the program")

    except KeyboardInterrupt:
        print("""
        ===============================
        Program was exited by the user
        ===============================
        """)

if __name__ == "__main__":
    main_engine()
    print("If any error occured and you don't know it's solution, feel free to report it as an issue at my github.\nLink to github: https://github.com/TheAbdulMuqeet")

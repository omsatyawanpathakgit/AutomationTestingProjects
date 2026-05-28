from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time


def type_search_results(query):
    global SEARCH_QUERY
    SEARCH_QUERY = query

# -------- SETUP DRIVER --------
from selenium.webdriver.chrome.service import Service
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

driver.maximize_window()

def open_website(url):
    driver.get(url)
    time.sleep(3)

def search_youtube():
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(SEARCH_QUERY)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)


def play_video_results():
    for i in range(1,10):
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "video-title"))
        )

        video = driver.find_element(By.XPATH, "(//ytd-video-renderer//a[@id='video-title'])"+f"[{i}]")
        print(video.text)
        video.click()

        # wait for video page
        time.sleep(5)

        # ---- CLICK SKIP AD WHEN IT APPEARS ----
        try:
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ytp-skip-ad-button"))
            ).click()
            print("Ad skipped")
        except:
            print("No skip ad button")
    

        time.sleep(50) # watch video for 50 seconds before scrolling down to end of page
        driver.back()  # go back to search results

 
def go_to_home_after_all_videos_played():
    driver.get("https://www.youtube.com")
    time.sleep(3)


def scroll_to_end_of_page():
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("Reached end of page")


type_search_results("Mohenjodaro documentary")
open_website("https://www.youtube.com")
search_youtube()
play_video_results()
go_to_home_after_all_videos_played()
scroll_to_end_of_page()

# -------- CLOSE BROWSER --------
time.sleep(5)
driver.quit()
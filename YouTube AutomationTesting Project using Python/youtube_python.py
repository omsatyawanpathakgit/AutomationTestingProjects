import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class YouTubeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # -------- LOGGING SETUP --------
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        cls.logger = logging.getLogger()

        # -------- DRIVER SETUP --------
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)

        cls.base_url = "https://www.youtube.com"
        cls.search_query = "Mohenjodaro documentary"

        cls.logger.info("Driver initialized successfully")

    def test_youtube_search_and_play(self):
        driver = self.driver
        wait = self.wait

        # -------- OPEN WEBSITE --------
        self.logger.info("Opening YouTube")
        driver.get(self.base_url)

        # -------- VERIFY PAGE LOAD --------
        self.assertIn("YouTube", driver.title)

        # -------- SEARCH --------
        self.logger.info(f"Searching for: {self.search_query}")
        search_box = wait.until(
            EC.presence_of_element_located((By.NAME, "search_query"))
        )
        search_box.send_keys(self.search_query)
        search_box.send_keys(Keys.ENTER)

        # -------- VERIFY SEARCH RESULTS --------
        videos = wait.until(
            EC.presence_of_all_elements_located((By.ID, "video-title"))
        )
        self.assertTrue(len(videos) > 0, "No search results found")

        self.logger.info(f"Found {len(videos)} videos")

        # -------- PLAY FIRST 5 VIDEOS --------
        for i in range(5):
            self.logger.info(f"Playing video {i+1}")

            videos = wait.until(
                EC.presence_of_all_elements_located((By.ID, "video-title"))
            )

            video_title = videos[i].text
            self.logger.info(f"Video Title: {video_title}")

            videos[i].click()

            # -------- WAIT FOR VIDEO PAGE --------
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "html5-video-player"))
            )

            # -------- TRY SKIP AD --------
            try:
                skip_btn = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "ytp-skip-ad-button"))
                )
                skip_btn.click()
                self.logger.info("Ad skipped")
            except:
                self.logger.info("No ad to skip")

            # -------- VALIDATION --------
            self.assertIn("youtube", driver.current_url.lower())

            # -------- WATCH SHORT TIME --------
            driver.implicitly_wait(3)

            # -------- GO BACK --------
            driver.back()

        self.logger.info("Test completed successfully")

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("Closing browser")
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
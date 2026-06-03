from selenium.webdriver import Chrome, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging
import time


def prepare_logs():
    log_file = r"complete___updated_apple_automationTesting_logs.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def test_using_github_actions():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return options


def load_apple_website():
    global driver, wait
    driver = Chrome(options=test_using_github_actions())

    # Mobile viewport like your DevTools screenshot
    driver.set_window_size(688, 1296)

    driver.get("https://www.apple.com/")

    wait = WebDriverWait(driver, 20)
    logging.info("Apple website opened")


def close_popup_if_present():
    try:
        popup_close = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "ac-ls-close"))
        )

        popup_close.click()

        time.sleep(4)
        
        logging.info("Country popup closed")
    except:
        logging.info("Country popup not found")





def scroll_to_footer():
    driver.execute_script("""
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
    """)

    time.sleep(5)

    logging.info("Scrolled to footer")


def scroll_to_top():
    driver.execute_script("""
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    """)

    time.sleep(5)

    logging.info("Scrolled to top")


def search_queries():
    search_queries_list = ["iPhone", "MacBook", "iPad", "Apple Watch", "AirPods"]

    for item in search_queries_list:
        try:
            search_icon = wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "globalnav-menubutton-link-search")
                )
            )
            search_icon.click()

            search_input = wait.until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "globalnav-searchfield-input")
                )
            )

            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.DELETE)

            search_input.send_keys(item)
            search_input.send_keys(Keys.ENTER)

            logging.info(f"Searched: {item}")

            time.sleep(4)

            scroll_to_footer()
            scroll_to_top()

        except Exception as e:
            logging.error(f"Search failed for {item}: {e}")

    

def open_sidebar_menu():
    try:
        menu_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "globalnav-menutrigger-button")
            )
        )
        menu_button.click()
        logging.info("Sidebar menu opened")

        # Close the sidebar menu after opening
        time.sleep(2)
        menu_button.click()
        logging.info("Sidebar menu closed")

    except Exception as e:
        logging.error(f"Failed to open sidebar menu: {e}")
        print("Failed to open sidebar menu")




def click_footer_section(section_name):
    try:

        button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//button[contains(.,'{section_name}')]"
                )
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        time.sleep(1)

        driver.execute_script(
            "arguments[0].click();",
            button
        )

        logging.info(f"Expanded {section_name}")

        time.sleep(2)

        # Re-find button before collapsing
        button = driver.find_element(
            By.XPATH,
            f"//button[contains(.,'{section_name}')]"
        )

        driver.execute_script(
            "arguments[0].click();",
            button
        )

        logging.info(f"Collapsed {section_name}")

        time.sleep(1)

    except Exception as e:
        logging.error(
            f"Failed to click {section_name}: {e}"
        )
        print(f"Failed to click {section_name}")












def main():

    prepare_logs()
    load_apple_website()
    test_using_github_actions()
    close_popup_if_present()

    open_sidebar_menu()

    scroll_to_footer()
    footer_sections = [
        "Shop and Learn",
        "Apple Wallet",
        "Account",
        "Entertainment",
        "Apple Store",
        "For Business",
        "For Education",
        "For Healthcare",
        "For Government",
        "Apple Values",
        "About Apple"
    ]
    for section in footer_sections:
        click_footer_section(section)

    time.sleep(5)

    scroll_to_top()


    search_queries()


    driver.quit()


main()
import os
from selenium.webdriver import Chrome, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging
import time


def save_screenshot(driver, filename, subfolder=None):
    
    current_folder = os.path.dirname(os.path.abspath(__file__))

    if subfolder:
        folder_path = os.path.join(current_folder, subfolder)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, filename)
    else:
        file_path = os.path.join(current_folder, filename)

    driver.save_screenshot(file_path)
    logging.info(f"Screenshot saved: {file_path}")
    print(f"Screenshot saved: {file_path}")

def prepare_logs():
    current_folder = os.path.dirname(os.path.abspath(__file__))

    log_file = os.path.join(
        current_folder,
        "OPERATIONS_HISTORY_ON_Apple_website.log"
    )

    abs_path = os.path.abspath(log_file)
    print(f"Log file will be created at: {abs_path}")

    logging.basicConfig(
        filename=log_file,
        filemode='w',
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
    driver.set_window_size(688, 1296)   # Mobile viewport
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

def test_site_to_enforce_https():
    try:
        driver.get("http://www.apple.com/")
        if driver.current_url.startswith("https"):
            print("Redirected to HTTPS successfully")
            logging.info("Redirected to HTTPS successfully")
        else:
            print("Redirection to HTTPS failed")
            logging.error("Redirection to HTTPS failed")
    except Exception as e:
        logging.error(f"Error while accessing Apple website: {e}")

def navigate_to_apple_sitemap():
    try:
        sitemap_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, "Site Map")
            )
        )
        sitemap_link.click()
        logging.info("Navigated to Apple sitemap")

        time.sleep(20)  # Wait for the sitemap page to load
        logging.info("Sitemap page loaded")

        
        # Use the new screenshot function
        save_screenshot(driver, "apple_sitemap_screenshot.png",subfolder="all_product_searchResults_screenshots")
        
        scroll_to_footer()
        scroll_to_top()

        driver.back()  # Go back to the previous page
        logging.info("Returned to previous page after viewing sitemap")
    except Exception as e:
        logging.error(f"Failed to navigate to Apple sitemap: {e}")
        print("Failed to navigate to Apple sitemap")

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
    search_queries_list = ["iPhone", "MacBook", "iPad", "Watch", "AirPods"]

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

            time.sleep(5)  # Wait for search results to load

            # Save screenshot using the helper function
            filename = f"{item}_searchResults_screenshot.png"
            save_screenshot(
                driver,
                filename,
                subfolder="all_product_searchResults_screenshots"
            )

            logging.info(f"Searched: {item}")
            print(f"Searched: {item}")

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

def navigate_to_login_page():
    try:
        # Go back to homepage first:
        driver.get("https://www.apple.com/")

        bag_icon = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "globalnav-menubutton-link-bag")
            )
        )
        bag_icon.click()

        time.sleep(2)  # Wait for the dropdown to appear
        account_icon = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a.ac-gn-bagview-nav-link-signin")
            )
        )
        account_icon.click()

        time.sleep(10)  # Wait for the login page to load
        logging.info("Navigated to login page")

        email_or_phone_input = wait.until(
            EC.presence_of_element_located(
                (By.ID, "account_name_text_field")
            )
        )

        email_or_phone_input.click()
        time.sleep(3)

        email_or_phone_input.send_keys("omsatyawanpathakwebdevelopment@gmail.com")
        email_or_phone_input.send_keys(Keys.ENTER)

        logging.info("Email entered")
        logging.info("Entered email on login page")
    except Exception as e:
        logging.error(f"Failed to navigate to login page (and/or) enter login details!")


def main():
    prepare_logs()
    load_apple_website()
    close_popup_if_present()
    test_site_to_enforce_https()
    navigate_to_apple_sitemap()

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

    navigate_to_login_page()

    driver.quit()   

if __name__ == "__main__":
    main()
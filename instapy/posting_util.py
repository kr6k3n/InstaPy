import time
from selenium.common.exceptions import NoSuchElementException, WebDriverException, ElementNotVisibleException


def post_to_instagram(browser, image_path, caption):

        """
        Posts Image from filepath to instanciated instagram account

        Expected Args:
            - image_path (full path to the picture path)
            - caption
        """
        #/html/body/div[4]/div/div/div[3]/button[2]
        check_connection()
        clicked = False
        while not clicked:
             try:
                 browser.find_element_by_xpath(
                     "//div[@role='menuitem']").click()
                 clicked = True
             except ElementNotVisibleException:
                 #sometimes a popup blocks a post button on the bottom
                 check_connection()
                 close_popups("/html/body/div[4]/div/div[2]/div/div[5]/button")

        input_elem = browser.find_element_by_xpath('//*[@id="react-root"]/form/input')
        input_elem.send_keys(image_path)
        check_connection()

        time.sleep(1)
        browser.find_element_by_xpath(
            "//button[contains(text(), 'Next')]").click()
        time.sleep(0.2)
        check_connection()

        browser.find_element_by_tag_name(
            "textarea").send_keys(caption)
        
        time.sleep(0.5)
        check_connection()

        browser.find_element_by_xpath(
            "//button[contains(text(), 'Share')]").click()
        #wait until it goes back to main page (until photo has been posted)
        while browser.current_url != "https://www.instagram.com/":
            time.sleep(0.1)

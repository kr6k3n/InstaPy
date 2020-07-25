import time
from .util import click_element
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException, ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains

def close_popups(browser, xpath):
    body = browser.find_element_by_css_selector('body')
    for _ in range(5):
        time.sleep(1)
        body.send_keys(Keys.PAGE_DOWN)
        try:
            click_element(browser, browser.find_element_by_xpath(xpath))
            break
        except:
            pass


def post_to_instagram(browser, image_path, caption, logger):
        """
        Posts Image from filepath to instanciated instagram account

        Expected Args:
            - browser instance
            - image_path (full path to the picture path)
            - caption
        """
        browser.implicitly_wait(3)
        clicked = False
        while not clicked:
             try:
                 post_button = browser.find_element_by_xpath("//div[@role='menuitem']")
                 click_element(browser,post_button)
                 clicked = True
             except ElementNotVisibleException:
                 #sometimes a popup blocks a post button on the bottom
                 close_popups(browser,"/html/body/div[4]/div/div[2]/div/div[5]/button")

        input_elem = browser.find_element_by_xpath('//*[@id="react-root"]/form/input')
        input_elem.send_keys(image_path)
        

        next_button = browser.find_element_by_xpath(
            "//button[contains(text(), 'Next')]")
        click_element(browser, next_button)
        

        caption_box = browser.find_element_by_tag_name("textarea")
        caption_box.send_keys(caption)
            

        share_button = browser.find_element_by_xpath( "//button[contains(text(), 'Share')]")
        click_element(browser, share_button)
        #wait until it goes back to main page (until photo has been posted)
        #TODO: relaunch sharing if sharing has not succeded
        while browser.current_url != "https://www.instagram.com/":
            time.sleep(0.1)
        return "Success"

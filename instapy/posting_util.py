import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException, ElementNotVisibleException

def close_popups(browser, xpath):
        for _ in range(5):
            time.sleep(3)
            browser.find_element_by_css_selector(
                'body').send_keys(Keys.PAGE_DOWN)
            try:
                browser.find_element_by_xpath(xpath).click()
                break
            except:
                pass

def check_connection(browser):
    try:
        for _ in range(10): 
            main_msg = browser.find_element_by_xpath(
                '//*[@id="main-message"]/h1/span')
            if main_msg == "This site can’t be reached":
                logger.debug("INSTABOT : Connection failed, refreshing")
                browser.refresh()
                time.sleep(10)
            else:
                break
        return 0
    except NoSuchElementException:
        logger.debug("INSTABOT : Couldn't find main msg so connection must be stable")

def post_to_instagram(browser, image_path, caption):

        """
        Posts Image from filepath to instanciated instagram account

        Expected Args:
            - browser instance
            - image_path (full path to the picture path)
            - caption
        """
        #/html/body/div[4]/div/div/div[3]/button[2]
        check_connection(browser)
        clicked = False
        while not clicked:
             try:
                 browser.find_element_by_xpath(
                     "//div[@role='menuitem']").click()
                 clicked = True
             except ElementNotVisibleException:
                 #sometimes a popup blocks a post button on the bottom
                 check_connection(browser)
                 close_popups(browser,"/html/body/div[4]/div/div[2]/div/div[5]/button")

        input_elem = browser.find_element_by_xpath('//*[@id="react-root"]/form/input')
        input_elem.send_keys(image_path)
        check_connection(browser)

        time.sleep(1)
        browser.find_element_by_xpath(
            "//button[contains(text(), 'Next')]").click()
        time.sleep(0.2)
        check_connection(browser)

        browser.find_element_by_tag_name(
            "textarea").send_keys(caption)
        
        time.sleep(0.5)
        check_connection(browser)

        browser.find_element_by_xpath(
            "//button[contains(text(), 'Share')]").click()
        #wait until it goes back to main page (until photo has been posted)
        while browser.current_url != "https://www.instagram.com/":
            time.sleep(0.1)
        return "Success"

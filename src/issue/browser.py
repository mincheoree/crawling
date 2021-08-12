from loguru import logger
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

from utils.option import get_chrome_option


class Browser:
    INIT_WAIT_TIME = 10

    driver: WebDriver

    def __init__(self, executable_path: str, is_headless=True) -> None:
        """
        only initialize
        """
        try:
            driver = webdriver.Chrome(
                executable_path=executable_path,
                options=get_chrome_option(is_headless),
            )
            WebDriverWait(driver, self.INIT_WAIT_TIME)
        except WebDriverException as err:
            logger.warning(err)
            # not a proper exception
            raise Exception('failed initialize web driver.')
        else:
            self.driver = driver

    def get_page(self, url: str) -> None:
        try:
            self.driver.get(url)
            # need to find more good way to wait
            WebDriverWait(self.driver, self.INIT_WAIT_TIME)
        except WebDriverException:
            self.driver.quit()
            raise Exception("site can't be reached")

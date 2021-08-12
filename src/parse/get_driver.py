import time

from selenium import webdriver
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.support.ui import WebDriverWait
from loguru import logger

from utils.option import get_chrome_option


class Driver:
    def __init__(self, url, path="../resources/chromedriver") -> None:
        self.url = url
        try:
                INIT_WAIT_TIME = 5
                self.driver = webdriver.Chrome(
                    executable_path=path, options=get_chrome_option(False)
                )
        except WebDriverException as err:
            logger.warning('failed get web driver')
            raise ValueError(err)
        else:
            try:
                WebDriverWait(self.driver, INIT_WAIT_TIME)
            except TimeoutException as err:
                logger.warning(f'timeout raise wait {INIT_WAIT_TIME} sec')
                logger.warning(err)
    
    def get_page(self) -> bool:
        """page를 접속할 수 있는지 확인하는 함수"""
        try:
            self.driver.get(self.url)
        except WebDriverException:
            logger.info("site can't be reached")
            self.driver.quit()
            return False
        else:
            return True

    def initialize(self):
        if not self.get_page():
                raise ValueError(f'failed get page from {self.url}')
                
        time.sleep(5)

    def get_driver(self): 
        return self.driver 
    

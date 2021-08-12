from __future__ import annotations
from typing import Callable, TYPE_CHECKING, Tuple

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from loguru import logger

from ..rule.constants import PathType
from .exceptions import FailedWorkException

if TYPE_CHECKING:
    from .spider_element import SpiderElement


class WaitSpider:
    """
    do not reference other spider module that can makes circular import error.

    TODO remove duplicated codes
    """

    def __init__(self, webdriver: WebDriver) -> None:
        if not webdriver:
            raise ValueError('web driver must be assigned.')
        self.__driver = webdriver

    @property
    def driver(self) -> WebDriver:
        return self.__driver

    def wait_element_visible(
        self, element: SpiderElement, wait_sec: float = 5.0
    ) -> WebElement:
        """
        TODO measure real taken time.
        """
        if not element:
            raise ValueError('must assign element.')

        web_element, path_type, path = self.__get_web_element_info(element)

        try:
            wait_element = WebDriverWait(self.driver, wait_sec).until(
                EC.visibility_of_element_located(
                    (self.__get_path_by(path_type, path))
                )
            )
        except TimeoutException:
            logger.debug(f'timeout raise while wait {path}')
            raise FailedWorkException(WaitSpider, self.wait_element)
        except WebDriverException as err:
            logger.debug(err)
            raise FailedWorkException(WaitSpider, self.wait_element)
        else:
            logger.debug(f'finished wait {path} can visible')
            return wait_element

    def wait_element_clickable(
        self, element: SpiderElement, wait_sec: float = 5.0
    ) -> WebElement:
        if not element:
            raise ValueError('must assign element.')

        web_element, path_type, path = self.__get_web_element_info(element)

        try:
            wait_element = WebDriverWait(self.driver, wait_sec).until(
                EC.element_to_be_clickable(
                    (self.__get_path_by(path_type, path))
                )
            )
        except TimeoutException:
            logger.debug(f'timeout raise while wait {path}')
            raise FailedWorkException(WaitSpider, self.wait_element_clickable)
        except WebDriverException as err:
            logger.debug(err)
            raise FailedWorkException(WaitSpider, self.wait_element_clickable)
        else:
            logger.debug(f'finished wait {path} can clickable.')
            return wait_element

    def __get_web_element_info(
        self, element: SpiderElement
    ) -> Tuple[str, str, str]:
        try:
            selenium = element.selenium
        except AttributeError as err:
            logger.debug(err)
            logger.warning(f'failed get selenium element from {element}')
            raise FailedWorkException(WaitSpider, self.__get_web_element_info)
        try:
            web_element = selenium.element
            path_type = selenium.path_type
            path = selenium.path
        except AttributeError as err:
            logger.warning(err)
            raise FailedWorkException(WaitSpider, self.__get_web_element_info)

        return web_element, path_type, path

    @staticmethod
    def __get_path_by(path_type: str) -> By:
        if path_type == PathType.SELECTOR:
            return By.CSS_SELECTOR
        elif path_type == PathType.XPATH or path_type == PathType.FULL_XPATH:
            return By.XPATH
        else:
            raise TypeError(f'given {path_type} is not defined.')

    def wait_page_loaded(self, wait_sec: float = 10.0) -> None:
        """
        try several way to check page loaded. not rendered.
        (currently we can not specified "rendered" state.)
        """
        try:
            WebDriverWait(self.driver, wait_sec).until(
                self.__is_document_ready_complete
            )
        except TimeoutException as err:
            logger.debug(err)
        except WebDriverException as err:
            logger.debug(err)
        else:
            return

        logger.warning('failed wait ready state when complete.')

    def __is_document_ready_complete(self) -> bool:
        """
        check document's "readyState" == "complete"
        """
        COMPLETE = 'complete'

        try:
            ready_state = self.driver.execute_script(
                "return document.readyState;"
            )
        except WebDriverException as err:
            logger.warning(err)
            return False
        else:
            logger.info(f'get ready state as {ready_state}.')
            return ready_state == COMPLETE

    def wait_element_stale(
        self, stale_element: WebElement, wait_sec=10.0
    ) -> None:
        """
        wait till element is stale or not.
        """
        try:
            WebDriverWait(self.driver, wait_sec).until(
                EC.staleness_of(stale_element)
            )
        except TimeoutException as err:
            logger.warning(f'timeout raised while wait {wait_sec}')
            logger.warning(err)
            raise FailedWorkException(WaitSpider, self.wait_element_stale)
        else:
            logger.debug('finished wait stale of element.')

from __future__ import annotations
import time
from typing import Union, TYPE_CHECKING

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote import webdriver
from selenium.webdriver.remote import webelement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable,
)
from loguru import logger

from .exceptions import FailedWorkException
from .wait_spider import WaitSpider

if TYPE_CHECKING:
    from .spider_element import SpiderElement


class ScrollPaginationSpider:
    """
    TODO
        change name to just ScrollSpider
    """

    __driver: WebDriver
    __scroll_position: float

    VISIBLE_WAIT_SEC = 10.0

    def __init__(self, webdriver: WebDriver):
        if not webdriver:
            raise ValueError('must assign webdriver.')

        self.__driver = webdriver
        self.__scroll_position = 0

    @property
    def driver(self) -> WebDriver:
        return self.__driver

    def move(
        self, count: int, is_downside=True, scroll_size=100.0
    ) -> Union[float, bool]:
        """
        scroll move count times method
        """
        if count <= 0:
            raise ValueError('count allowed only positive number.')

        for _ in range(1, count + 1):
            if is_downside:
                scroll_position = self.move_downside(scroll_size)
                if not scroll_position:
                    return False
                else:
                    self.__update_scroll_position(scroll_position)
            else:
                raise NotImplementedError('scroll up is not supported yet.')

        return self.__scroll_position

    def __get_scroll_position(self) -> float:
        """this method use JS excute"""
        return self.__driver.execute_script(
            'return window.scrollY || window.scrollTop || document.getElementsByTagName("html")[0].scrollTop;'
        )

    def move_downside(self, scroll_size: float) -> Union[float, bool]:
        """
        this method cause a not expected result
        which is scroll down bottom of page. that makes not load data.

        TODO remove hard time wait
        """
        try:
            dest_scroll_position = self.__scroll_position + scroll_size
            logger.debug(f'trying to move {dest_scroll_position}')
            self.__driver.execute_script(
                f"window.scrollTo(0, {dest_scroll_position});"
            )
        except Exception as err:
            logger.debug('failed scroll down', err)
            return False
        else:
            time.sleep(0.05)

        scroll_position = self.__get_scroll_position()
        if self.__scroll_position >= scroll_position:
            logger.debug('failed scroll down. scroll position is not changed.')

        return scroll_position

    def __update_scroll_position(self, scroll_position: float = 0):
        """
        explicitly update scroll position
        """

        if scroll_position:
            self.__scroll_position = scroll_position
        else:
            self.__scroll_position = self.__get_scroll_position()

    def scroll_into_view(self, element: SpiderElement) -> None:
        """
        try 2 way metho to scroll into view
        1. use actionchain in selenium
        2. use JS excute script
        """
        if not self.__actionchain_scroll_into_view(element):
            if not self.__js_scroll_into_view(element):
                raise FailedWorkException(
                    ScrollPaginationSpider, self.scroll_into_view
                )

        logger.info('succeed scroll into view element.')
        logger.debug(f'scroll target element {element}')

    def __js_scroll_into_view(self, element: SpiderElement) -> bool:
        """
        use JS .scrollIntoView(true) method. this method use selenium's WebElement.
        if failed get selenium element can not progress.
        when failed return False.
        """
        try:
            selenium = element.selenium
            selenium_element = selenium.element
        except AttributeError as err:
            logger.warning(err)
            raise FailedWorkException(
                ScrollPaginationSpider, self.__js_scroll_into_view
            )
        else:
            try:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", selenium_element
                )
            except WebDriverException as err:
                logger.warning(err)
                return False
            else:
                self.__wait_till_element_visible(element)
                return True

    def __actionchain_scroll_into_view(
        self, element: SpiderElement, path_type: str, path: str
    ) -> bool:
        """
        TODO add possible exception. current we do not know which exception can raised.
        """
        from selenium.webdriver.common.action_chains import ActionChains

        webelement = element.selenium.element
        try:
            ActionChains(self.driver).move_to_element(webelement).perform()
        except WebDriverException as err:
            logger.debug(err)
            return False
        else:
            self.__wait_till_element_visible(element)
            return True

    def __wait_till_element_visible(self, element: SpiderElement) -> None:
        try:
            wait_spider = WaitSpider(self.driver)
            wait_spider.wait_element_visible(element, self.VISIBLE_WAIT_SEC)
        except FailedWorkException as err:
            logger.warning(err)
            logger.warning(f'failed wait {element} but scroll finished.')

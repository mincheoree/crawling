from typing import List
import time
import csv

from loguru import logger
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchAttributeException,
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
)

from .browser import Browser

"""
[issued link](https://github.com/xoxwgys56/spiderkim-cwl-modules/issues/16)
"""


def scraper(path: str, export_file_path: str) -> bool:
    INIT_WAIT_TIME = 10
    url = "https://www.pinterest.co.kr/dogs/"
    scroll_count = 5

    try:
        browser = Browser(path)
        browser.get_page(url)
    except Exception as err:
        logger.error(err)
        return False

    try:
        csv_file = open(export_file_path, "w", encoding="utf-8-sig", newline="")
    except OSError as err:
        logger.warning(f'failed open {export_file_path} file.')
        logger.error(err)
        return False
    else:
        # scroll to target page
        try:
            scroll_to_target_count(browser.driver, scroll_count)
        except WebDriverException as err:
            logger.warning(
                f"failed scroll down {scroll_count} times. failed scraping"
            )
            logger.error(err)
            return False
        else:
            # parsing data
            try:
                parsing_data(browser.driver, csv_file)
            except ValueError as err:
                logger.warning('failed parinsg pinterest.')
                logger.error(err)
                return False
            else:
                browser.driver.quit()
                logger.info("pinterest scraping finished.")
                return True
    finally:
        csv_file.close()


def parsing_data(driver: WebDriver, csv_file) -> bool:
    writer = csv.DictWriter(
        csv_file, fieldnames=["title", "summary", "image src"]
    )
    writer.writeheader()

    try:
        content_element: WebElement = driver.find_element_by_xpath(
            '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[1]/div[2]/div/div/section/div/div[1]/div'
        )
    except NoSuchElementException:
        raise ValueError("failed get content element. can not progress")

    element_list: List[
        WebElement
    ] = content_element.find_elements_by_class_name("Collection-Item")
    logger.info(f"grep {len(element_list)} elements")

    # item = '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[1]/div[2]/div/div/section/div/div[1]/div/div/div[4]'
    # title = '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[1]/div[2]/div/div/section/div/div[1]/div/div/div[4]/div/div[2]/figcaption/h3'
    # summary = '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[1]/div[2]/div/div/section/div/div[1]/div/div/div[4]/div/div[2]/div[3]/p'
    # image = '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[1]/div[2]/div/div/section/div/div[1]/div/div/div[4]/div/div[1]/div[1]/a/img'

    for element in element_list:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.implicitly_wait(1)

        try:
            title = element.find_element_by_xpath(
                "div/div[2]/figcaption/h3"
            ).text
        except NoSuchElementException:
            title = ""
            logger.debug("No title element")
        try:
            summary = element.find_element_by_xpath("div/div[2]/div[3]/p").text
        except NoSuchElementException:
            summary = ""
            logger.debug("No summary element")

        try:
            image_src = element.find_element_by_xpath(
                "div/div[1]/div[1]/a/img"
            ).get_attribute("src")
        except NoSuchElementException:
            image_src = ""
            logger.debug("No image src element")
        except NoSuchAttributeException:
            image_src = ""
            logger.debug('no src value from element')

        parsed_item = {
            "title": title,
            "summary": summary,
            "image src": image_src,
        }

        writer.writerow(parsed_item)

    return True


def scroll_to_target_count(driver: WebDriver, target_count: int):
    """
    scroll down to bottom of page.
    after scroll down, scroll up to top of page.
    """
    SCROLL_PAUSE_SEC = 1.5
    ALARM_WAIT_SEC = 3

    SCROLL_UP_WAIT = 0.5

    content_class_name = "Collection"

    for count in range(target_count):
        logger.info(f"scroll {count} times")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, content_class_name)
                )
            )
        except WebDriverException as err:
            logger.error(err)
            raise Exception('failed wait 10 sec')
        except TimeoutError as err:
            logger.error(err)
            raise Exception(
                f'there is timeout error raised while wait {content_class_name}'
            )

        # last height
        last_height = driver.execute_script("return document.body.scrollHeight")
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        try:
            WebDriverWait(driver, ALARM_WAIT_SEC).until(
                EC.alert_is_present(),
                "Timed out waiting for PA creation confirmation popup to appear.",
            )
            alert = driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            logger.debug("no alert")
        else:
            logger.info("alert accepted")

    driver.execute_script("window.scrollTo(0, 0);")
    driver.implicitly_wait(SCROLL_UP_WAIT)

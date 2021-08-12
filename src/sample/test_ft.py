import json
import csv

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from loguru import logger


def test_scraper(get_page):
    driver = get_page

    WAIT_TIME = 3

    #### Accept the cookie popups
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div[1]/div/div[1]/div/div/div/div[2]/div[1]",
            )
        )
    ).click()

    WebDriverWait(driver, WAIT_TIME)

    with open(export_file_path, "w", encoding="utf-8-sig", newline="") as f:

        for p_count in range(0, 12):

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="stream"]/div[1]/ul')
                )
            )

            elem = driver.find_element_by_xpath('//*[@id="stream"]/div[1]/ul')

            ### Need to wait until the lists are loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "o-grid-row"))
            )

            lists = elem.find_elements_by_class_name("o-grid-row")

            logger.debug(f"PAGE NUMBER: {p_count}")

            for list in lists:
                try:
                    date = list.find_element_by_class_name(
                        "stream-card__date"
                    ).text
                except NoSuchElementException:
                    date = ""
                    logger.info("date is same as previous article")
                try:
                    category = list.find_element_by_class_name(
                        "o-teaser__meta"
                    ).text
                except NoSuchElementException:
                    category = ""
                    logger.info("category not found")
                try:
                    heading = list.find_element_by_class_name(
                        "o-teaser__heading"
                    ).text
                except NoSuchElementException:
                    heading = ""
                    logger.info("heading not found")
                try:
                    content = list.find_element_by_class_name(
                        "o-teaser__standfirst"
                    ).text
                except NoSuchElementException:
                    content = ""
                    logger.info("heading not found")

                parsed_item = {
                    "date": date,
                    "category": category,
                    "heading": heading,
                    "content": content,
                }
                logger.info(json.dumps(parsed_item, indent=4, sort_keys=True))

                writer.writerows([parsed_item])

            #### deal with No button element error
            try:
                button = driver.find_element_by_class_name(
                    "o-buttons-icon--arrow-right"
                )
            except NoSuchElementException:
                logger.info("Page reacheds the end")
                logger.info("financial times scraping finished.")
                driver.quit()
                return True

                ##### Used for button click intercept error
            driver.execute_script("arguments[0].click();", button)

            #### deal with alerts
            try:
                WebDriverWait(driver, 3).until(
                    EC.alert_is_present(),
                    "Timed out waiting for PA creation "
                    + "confirmation popup to appear.",
                )

                alert = driver.switch_to.alert
                alert.accept()
                logger.info("alert accepted")
            except TimeoutException:
                logger.warning("no alert")

    driver.quit()
    logger.info("financial times scraping finished.")
    return True

from typing import Counter
import json
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru import logger

from utils.option import get_chrome_option


def scraper(path: str, export_file_path: str) -> bool:
    driver = webdriver.Chrome(executable_path=path, options=get_chrome_option())
    fieldnames = ["title", "category", "constructors", "rating", "course_info"]

    driver.get("https://www.udemy.com/courses/search/?src=ukw&q=python")
    WAIT_TIME = 3
    WebDriverWait(driver, WAIT_TIME)

    with open(export_file_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for p_count in range(0, 31):

            path = './/*[@id="udemy"]/div[2]/div[4]/div/div/div[2]/div[2]'
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, path))
            )

            page_bar = driver.find_element_by_xpath(
                './/*[@id="udemy"]/div[2]/div[4]/div/div/div[2]/div[2]'
            ).find_element_by_class_name("pagination--next--5NrLo")

            #### wait for loading the contents of webpage
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "course-list--container--3zXPS")
                )
            )
            elem = driver.find_element_by_class_name("course-list--container--3zXPS")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "popper--popper-hover--4YJ5J")
                )
            )
            lists = elem.find_elements_by_class_name("popper--popper-hover--4YJ5J")

            logger.debug(f"PAGE NUMBER: {p_count}")

            for list in lists:
                title = list.find_element_by_class_name(
                    "course-card--course-title--2f7tE"
                ).text
                category = list.find_element_by_class_name(
                    "course-card--course-headline--yIrRk"
                ).text
                constructors = list.find_element_by_class_name(
                    "course-card--instructor-list--lIA4f"
                ).text
                rating = list.find_element_by_class_name(
                    "star-rating--star-wrapper--2eczq"
                ).text
                course_info = list.find_element_by_class_name(
                    "course-card--course-meta-info--1hHb3"
                ).text

                parsed_item = {
                    "title": title,
                    "category": category,
                    "constructors": constructors,
                    "rating": rating,
                    "course_info": course_info,
                }
                logger.info(json.dumps(parsed_item, indent=4, sort_keys=True))

                writer.writerows([parsed_item])

            page_bar.click()

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

            ##add the count

    driver.quit()
    logger.info("petition scraping finished.")
    return True

import json
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru import logger

from utils.option import get_chrome_option


def scraper(path: str, export_file_path: str) -> bool:
    driver = webdriver.Chrome(executable_path=path, options=get_chrome_option())

    fieldnames = ["heading", "date", "content"]

    driver.get("https://edition.cnn.com/search?size=10&q=covid%20blues&page=1")
    WAIT_TIME = 3
    WebDriverWait(driver, WAIT_TIME)

    with open(export_file_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for p_count in range(0, 31):

            page_bar = driver.find_elements_by_css_selector("div.pagination-bar > *")

            WebDriverWait(driver, WAIT_TIME)

            elem = driver.find_element_by_xpath(
                "/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]"
            )

            lists = elem.find_elements_by_class_name("cnn-search__result")

            logger.debug(f"PAGE NUMBER: {p_count}")

            for list in lists:
                title = list.find_element_by_class_name(
                    "cnn-search__result-headline"
                ).text
                date = list.find_element_by_class_name(
                    "cnn-search__result-publish-date"
                ).text
                content = list.find_element_by_class_name(
                    "cnn-search__result-body"
                ).text
                content = " ".join(content.split()[:100])

                parsed_item = {"heading": title, "date": date, "content": content}
                logger.info(json.dumps(parsed_item, indent=4, sort_keys=True))

                writer.writerows([parsed_item])

            if p_count == 3:
                break

            page_bar[2].click()

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
            p_count += 1

    driver.quit()
    logger.info("cnn scraping finished.")
    return True

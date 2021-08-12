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
    fieldnames = ["number", "category", "content"]

    driver.get("https://www1.president.go.kr/petitions")
    WAIT_TIME = 3
    WebDriverWait(driver, WAIT_TIME)

    with open(export_file_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for p_count in range(0, 31):

            elem = driver.find_element_by_xpath(
                './/*[@id="cont_view"]/div[2]/div/div/div[2]/div[2]/div[4]/div/div[2]/div[2]/ul'
            )
            lists = elem.find_elements_by_tag_name("li")

            logger.debug(f"PAGE NUMBER: {p_count}")

            for list in lists:
                number = list.find_element_by_class_name("bl_no").text
                classifier = list.find_element_by_class_name("bl_category").text
                text = list.find_element_by_class_name("bl_subject").text

                parsed_item = {
                    "number": number,
                    "category": classifier,
                    "content": text,
                }
                logger.info(json.dumps(parsed_item, indent=4, sort_keys=True))

                writer.writerows([parsed_item])

            page_bar = driver.find_elements_by_css_selector("div.p_btn > *")

            if p_count < 10:
                page_bar[p_count + 1].click()
            else:
                page_bar[p_count % 10 + 2].click()

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
    logger.info("petition scraping finished.")
    return True

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

    fieldnames = ["id_no", "category", "title", "author", "추천수", "조회수", "날짜"]

    driver.get("https://bbs.ruliweb.com/news/board/11")

    WAIT_TIME = 3
    WebDriverWait(driver, WAIT_TIME)

    with open(export_file_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p_count in range(0, 31):

            page_bar = driver.find_elements_by_css_selector("div.paging_wrapper > *")
            WebDriverWait(driver, WAIT_TIME)
            elem = driver.find_element_by_xpath(
                '//*[@id="board_list"]/div/div[2]/table/tbody'
            )

            lists = elem.find_elements_by_tag_name("tr")
            logger.debug("PAGE NUMBER: " + str(p_count) + "\n")
            for list in lists:
                id_no = list.find_element_by_class_name("id").text
                category = list.find_element_by_class_name("divsn").text
                text = list.find_element_by_class_name("subject").text
                author = list.find_element_by_class_name("writer").text
                recommend = list.find_element_by_class_name("recomd").text
                count = list.find_element_by_class_name("hit").text
                date = list.find_element_by_class_name("time").text

                parsed_item = {
                    "id_no": id_no,
                    "category": category,
                    "title": text,
                    "author": author,
                    "추천수": recommend,
                    "조회수": count,
                    "날짜": date,
                }
                logger.info(json.dumps(parsed_item, indent=4, sort_keys=True))

                writer.writerows([parsed_item])

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

            ##add the count

    driver.quit()
    logger.info("ruli scraping finished.")
    return True

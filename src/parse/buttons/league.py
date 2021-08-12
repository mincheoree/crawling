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

    fieldnames = ["id_no", "title", "author", "date", "조회수", "추천수"]

    driver.get("https://gall.dcinside.com/board/lists/?id=leagueoflegends3")
    WAIT_TIME = 3
    WebDriverWait(driver, WAIT_TIME)

    with open(export_file_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        p_count = 0
        while p_count < 31:

            page_bar = driver.find_elements_by_css_selector("div.bottom_paging_box > *")

            WebDriverWait(driver, WAIT_TIME)

            elem = driver.find_element_by_xpath(
                './/*[@id="container"]/section[1]/article[2]/div[2]/table/tbody'
            )
            lists = elem.find_elements_by_tag_name("tr")

            logger.debug("PAGE NUMBER: " + str(p_count) + "\n")
            for list in lists:

                id_no = list.find_element_by_class_name("gall_num").text
                text = list.find_element_by_class_name("gall_tit").text
                author = list.find_element_by_class_name("gall_writer").text
                date = list.find_element_by_class_name("gall_date").text
                count = list.find_element_by_class_name("gall_count").text
                recommend = list.find_element_by_class_name("gall_recommend ").text
                ##### when n = 15, 31, 46, scrap nothing on the page
                if p_count == 15 or (p_count > 30 and p_count % 15 == 1):
                    continue
                else:

                    parsed_item = {
                        "id_no": id_no,
                        "title": text,
                        "author": author,
                        "date": date,
                        "조회수": count,
                        "추천수": recommend,
                    }
                    logger.info(json.dumps(parsed_item, indent=4, sort_keys=True))
                    writer.writerows([parsed_item])

            #####press the next page button
            if p_count < 15:
                page_bar[p_count + 1].click()
            else:
                ####when n =30, 45, we press the next button
                if p_count % 15 == 0 and n != 15:
                    page_bar[15 + 2].click()
                else:
                    if p_count > 30:
                        page_bar[p_count % 15 + 1].click()
                    else:
                        page_bar[p_count % 15 + 2].click()

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

            p_count += 1

    driver.quit()
    logger.info("dcinside scraping finished.")
    return True

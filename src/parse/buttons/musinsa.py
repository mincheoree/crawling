import json
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from loguru import logger

from utils.option import get_chrome_option


def scraper(path: str, export_file_path: str) -> bool:

    driver = webdriver.Chrome(executable_path=path, options=get_chrome_option())

    fieldnames = ["sale", "state", "brand", "cloth", "price", "rating", "heart"]

    driver.get(
        "https://search.musinsa.com/category/001005?category=&d_cat_cd=001005&u_cat_cd=&brand=&sort=pop&sub_sort=&display_cnt=80&page=1&page_kind=category&list_kind=small&free_dlv=&ex_soldout=&sale_goods=&exclusive_yn=&price=&color=&a_cat_cd=&sex=&size=&tag=&popup=&brand_favorite_yn=&goods_favorite_yn=&blf_yn=&price1=&price2=&brand_favorite=&goods_favorite=&chk_exclusive=&chk_sale=&chk_soldout="
    )
    WAIT_TIME = 3

    WebDriverWait(driver, WAIT_TIME)

    with open(export_file_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for p_count in range(0, 31):

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="searchList"]'))
            )
            elem = driver.find_element_by_xpath('//*[@id="searchList"]')

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "li_box"))
            )
            lists = elem.find_elements_by_class_name("li_box")

            logger.debug("\n" + "PAGE NUMBER: " + str(p_count) + "\n")

            for list in lists:
                try:
                    sale = list.find_element_by_class_name("icon_new").text
                except NoSuchElementException:
                    sale = ""
                    logger.debug("Element is not found")

                try:
                    state = list.find_element_by_class_name("box-icon-right").text
                except NoSuchElementException:
                    state = ""
                    logger.debug("Element is not found")
                brand = list.find_element_by_class_name("item_title").text
                cloth = list.find_element_by_class_name("list_info").text
                price = list.find_element_by_class_name("price").text

                try:
                    rating = list.find_element_by_class_name("point").text
                except NoSuchElementException:
                    rating = ""
                    logger.debug("Element is not found")

                try:
                    heart = list.find_element_by_class_name("txt_cnt_like").text
                except NoSuchElementException:
                    heart = ""
                    logger.debug("Element is not found")

                parsed_item = {
                    "sale": sale,
                    "state": state,
                    "brand": brand,
                    "cloth": cloth,
                    "price": price,
                    "rating": rating,
                    "heart": heart,
                }
                logger.info(json.dumps(parsed_item, indent=4, sort_keys=True))

                writer.writerows([parsed_item])

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, './/*[@id="goods_list"]/div[2]/div[5]/div')
                )
            )

            page_div = driver.find_element_by_xpath(
                './/*[@id="goods_list"]/div[2]/div[5]/div'
            )

            page_bar = page_div.find_elements_by_css_selector("div.wrapper > *")

            page_bar[p_count % 10 + 3].click()

            try:
                WebDriverWait(driver, 1).until(
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
    logger.info("musinsa scraping finished.")
    return True

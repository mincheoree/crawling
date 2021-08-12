import csv
import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from loguru import logger

from utils.option import get_chrome_option


def scraper(path: str, export_file_path: str) -> bool:
    """
    NOTE
        리턴 타입을 명시적으로 type hinting 해주시면 함수를 사용하는 쪽에서 편하다고 생각합니다.
        알고 계시듯이 작성하지 않아도, 문법적으로 아무런 오류가 없습니다.
        https://docs.python.org/ko/3/library/typing.html

    TODO
        `+`로 표시된 내역은 부가적인 사항입니다.

        - `time.sleep()`을 사용하지 마시고, `WebDriverWait`로 변경해주세요.
        - snake_case 변수명을 작성해주시고, 자주 사용되는 변수에 대해 `n`으로 선언된 변수는 다른 이름으로 변경해주세요.
            - https://stackoverflow.com/questions/159720/what-is-the-naming-convention-in-python-for-variable-and-function-names
        - driver.get() 실패했을 경우 예외처리해주세요.
        - chromeoption 추가해주세요. (src/util/option.py 참고해주세요.)
        - wait time을 상수로 선언해주세요.
        - 작성하신 코드에 대한 간단한 설명을 주석으로 작성해주세요. 각 코드에 대해 설명이 필요한 부분은 코드에, 함수에 대한 설명은 이렇게 doc string으로 작성해주셔도 좋습니다.

        + 함수 이름을 통해 어떤 동작을 하는지 알려주세요.
    """
    driver = webdriver.Chrome(executable_path=path, options=get_chrome_option())
    fieldnames = ["기사제목", "작성시간", "기사 내용", "카테고리", "저자"]

    try:
        driver.get(
            "https://www.donga.com/news/search?check_news=1&more=1&sorting=1&range=1&search_date=&v1=&v2=&query=corona"
        )
    except WebDriverException:
        logger.info("site can't be reached")
        driver.quit()
        return True

    #  "https://www.donga.com/news/search?check_news=1&more=1&sorting=1&range=1&search_date=&v1=&v2=&query=corona"
    WAIT_TIME = 3

    WebDriverWait(driver, WAIT_TIME)

    with open(export_file_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # 변수 이름을 좀 더 알아보기 좋게 변경해주세요.
        p_count = 0

        # 이 코드는 왜 중복 호출되는건가요?
        temp = []
        while p_count < 31:

            page_bar = driver.find_elements_by_css_selector("div.page > *")

            WebDriverWait(driver, WAIT_TIME)
            elem = driver.find_element_by_xpath('.//*[@id="content"]/div[3]/div[1]')

            lists = elem.find_elements_by_class_name("searchList")

            logger.info(f"PAGE NUMBER: {p_count}")

            for list in lists:
                title = (
                    list.find_element_by_class_name("tit")
                    .find_element_by_tag_name("a")
                    .text
                )
                date = (
                    list.find_element_by_class_name("tit")
                    .find_element_by_tag_name("span")
                    .text
                )
                content = list.find_element_by_class_name("txt").text
                category = (
                    list.find_element_by_class_name("loc")
                    .find_element_by_tag_name("em")
                    .text
                )

                ####Deal with element not found exceptions
                try:
                    author = (
                        list.find_element_by_class_name("loc")
                        .find_element_by_tag_name("span")
                        .text
                    )
                except NoSuchElementException:
                    author = ""
                    logger.debug("Element is not found")

                parsed_item = {
                    "기사제목": title,
                    "작성시간": date,
                    "기사 내용": content,
                    "카테고리": category,
                    "저자": author,
                }
                logger.info(json.dumps(parsed_item, indent=4, sort_keys=True))

                writer.writerows([parsed_item])

            # if (p_count + 1) == len(page_bar):
            #     """
            #     버튼 수로 판단하는 로직은 좋은 생각입니다.
            #     하지만 이 로직은 다른 웹페이지에서 오류가 발생할 수 있다고 보입니다.

            #     예를 들어, 11페이지로 접근할 때 아래와 같이
            #     1 2 3 4 5 6 7 8 9 10 next 인 경우, 총 11개의 요소가 있을 수 있습니다.
            #     이런 경우 버튼 수로 판단하는 것은 적절하지 않다고 생각합니다. (테스트해보진 않았습니디!)

            #     이 로직을 진행하신 다른 웹사이트에도 적용해봐주세요.
            #     """
            #     logger.info(f"{p_count+1} is same as {page_bar}")
            #     break
            # else:
            #     page_bar[p_count + 1].click()

            temp.append(len(lists))
            if temp[p_count - 1] > temp[p_count]:
                logger.info(f"Page{p_count} is at the end of the website!")

                break

            else:
                page_bar[p_count + 1].click()

            try:
                WebDriverWait(driver, WAIT_TIME).until(
                    EC.alert_is_present(),
                    "Timed out waiting for PA creation "
                    + "confirmation popup to appear.",
                )

                alert = driver.switch_to.alert
                alert.accept()
            except TimeoutException:
                logger.warning("no alert")
            else:
                logger.info("alert accepted")

            ##add the count
            p_count += 1

    driver.quit()
    logger.info("donga scraping finished.")
    return True

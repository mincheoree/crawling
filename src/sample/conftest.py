from typing import Tuple

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


url_list = [("https://www.ft.com/world",)]
"""
path must be selector
"""


@pytest.fixture(
    scope="function",
    params=url_list,
)
def get_page(request) -> WebDriver:
    DRIVER_WAIT_SEC = 5.0

    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--lang=ko_KR")

    try:
        driver = Chrome(
            executable_path='../resources/chromedriver', options=chrome_options
        )
    except WebDriverException as err:
        print(err)
        print('failed init chrome')
        yield None
    else:
        print('succeed init chrome')

    try:
        driver.get(request.param[0])
    except WebDriverException as err:
        print(err)
        print(f'failed get {request.param[0]}')
        yield None
    else:
        print('succeed get page.')

    # try:
    #     WebDriverWait(driver, DRIVER_WAIT_SEC).until(
    #         EC.presence_of_all_elements_located(
    #             (By.CSS_SELECTOR, request.param[1])
    #         )
    #     )
    # except TimeoutError as err:
    #     print(f'failed wait {DRIVER_WAIT_SEC} sec. timeout raised')
    #     yield driver
    # except WebDriverException as err:
    #     print(err)
    #     yield None
    # else:
    #     yield driver
    yield driver
    driver.quit()

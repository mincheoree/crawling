from selenium.webdriver.chrome.options import Options as ChromeOptions
from loguru import logger


def get_chrome_option(is_headless: bool = True) -> ChromeOptions:
    """
    generate chrome option
    :param is_headless: if true, use headless
    :return: chrome option
    """
    chrome_options = ChromeOptions()

    if is_headless:
        logger.info("set headless. no GUI browser popup.")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--single-process")
    else:
        logger.info("use GUI browser.")


    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--lang=ko_KR")

    return chrome_options

import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from loguru import logger

from parse.parsing import Parser
from parse.get_driver import Driver



class Crawler:
    def __init__(
        self,
        url,
        fieldnames,
        selectors,
        parent,
        is_dynamic: bool,
        child,
        site_name,
        backup_selectors = [],
        backup_parent= "",
        backup_child="",
    ):
        """
        initialize crawler. parameters initializing.
        if failed initialize raise ValueError

        :param url: 가져와야 되는 url
        :param fieldnames: csv file에 heading이자 가져오고 싶은 data 이름들
        :param selectors: list 안에서 가져오고 싶은 data를 찾기 위한 selector list, fieldname과 순서 같음
        :param parent: 웹페이지의 content element 이자 lists 들을 child로 가지고 있는 parent element를 찾기위한 parent selector
        :param is_dynamic: 웹페이지가 동적 selector를 포함하는지 안하는지 bool
        :param child: 웹페이지의 content element의 child, lists element를 찾는 child selector
        :param site_name: site 이름
        :param path: chromedriver path
        """
        # 파라미터들을 pass 해줌
        self.url = url
        self.fieldnames = fieldnames
        self.selectors = selectors
        self.parent = parent
        self.is_dynamic = is_dynamic
        self.child = child
        self.site_name = site_name
        self.backup_selectors = backup_selectors
        self.backup_parent = backup_parent
        self.backup_child = backup_child

        web_driver = Driver(self.url)
        web_driver.initialize()
        self.driver = web_driver.get_driver()
        
    def scraper(self, export_file_path: str):
        """scraper 함수, 객체의 scraping을 진행할 때 필요한 함수입니다"""

        scroll_count = 5
        #### open the csv file
        try:
            csv_file = open(
                export_file_path, "w", encoding="utf-8-sig", newline=""
            )
        except OSError as err:
            logger.warning(err)
        else:
            # scroll to target page
            try:
                scroll_to_target_count(
                    self.driver,
                    scroll_count,
                    self.parent,
                    self.is_dynamic,
                    self.child,
                )
            except WebDriverException as err:
                logger.error(f"failed scroll down {scroll_count} times.")
                if len(self.backup_selectors) != 0: 
                        scroll_to_target_count(
                            self.driver,
                            scroll_count,
                            self.backup_parent,
                            self.is_dynamic,
                            self.backup_child,
                        )

                        Parser(self.driver,
                        csv_file,
                        self.fieldnames,
                        self.backup_parent,
                        self.backup_child,
                        self.backup_selectors,
                        self.is_dynamic,
                        scroll_count,).parse_scroll()

                        logger.debug("Backup selectors scraping worked")
                else:
                    logger.error(err)
            else:
                try: 
                    Parser(self.driver,
                        csv_file,
                        self.fieldnames,
                        self.parent,
                        self.child,
                        self.selectors,
                        self.is_dynamic,
                        scroll_count,).parse_scroll()
                except TimeoutException:
                    logger.warning(err)
                else:
                    logger.info("finished parsing data.")
        finally:
            csv_file.close()

        self.driver.quit()
        logger.info(f"{self.site_name} scraping finished.")
        return True


def scroll_to_target_count(
    driver: WebDriver,
    target_count: int,
    parent: str,
    is_dynamic: bool,
    child: str,
):
    """
    scroll down to bottom of page.
    after scroll down, scroll up to top of page.
    """
    SCROLL_PAUSE_SEC = 3
    ALARM_WAIT_SEC = 3

    SCROLL_UP_WAIT = 0.5

    for count in range(target_count):
        logger.debug(f"PAGE NUMBER: {count}")
        if is_dynamic:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, parent[1:] + str(count + 1))
                )
            )
        
        WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, child))
                )
            
        logger.debug(f"PAGE: {count} element is located.")

        last_height = driver.execute_script(
            "return document.body.scrollHeight"
        )
        # 끝까지 스크롤 다운
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script(
            "return document.body.scrollHeight"
        )
        if new_height == last_height:
            break
        last_height = new_height

        try:
            WebDriverWait(driver, ALARM_WAIT_SEC).until(
                EC.alert_is_present(),
                "Timed out waiting for PA creation confirmation popup to appear.",
            )
            alert = driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            logger.debug("no alert")
        else:
            logger.info("alert accepted")

    driver.execute_script("window.scrollTo(0, 0);")
    driver.implicitly_wait(SCROLL_UP_WAIT)



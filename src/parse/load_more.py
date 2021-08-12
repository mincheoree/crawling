from loguru import logger
from parse.finder import Finder 
from parse.parsing import Parser
from parse.get_driver import Driver
import time

"""
    this class consider two cases
    1. click multiple times and parsing data -> Usually 'Load More' button
    2. parsing data while clicking   -> Pagination, usually 'Next' button
    """

class More:
    def __init__(
        self,
        url : str,
        fieldnames : list,
        selectors : list,
        parent : str,
        child : str,
        page_change : bool,
        button_selector : str,
        site_name : str,
    ):
        """
        initialize crawler. parameters initializing.
        if failed initialize raise ValueError

        :param url: 가져와야 되는 url
        :param fieldnames: csv file에 heading이자 가져오고 싶은 data 이름들
        :param selectors: list 안에서 가져오고 싶은 data를 찾기 위한 selector list, fieldname과 순서 같음
        :param parent: 웹페이지의 content element 이자 lists 들을 child로 가지고 있는 parent element를 찾기위한 parent selector
        :param child: 웹페이지의 content element의 child, lists element를 찾는 child selector
        :param page_change: 버튼 클릭할때 마다 기존 페이지가 다음 페이지로 넘어가는지 판단하는 bool 
        :param site_name: site 이름
        :param path: chromedriver path
        """
        self.url = url
        self.fieldnames = fieldnames
        self.selectors = selectors
        self.parent = parent
        self.child = child
        self.page_change = page_change
        self.button_selector = button_selector
        self.site_name = site_name
        
        web_driver = Driver(self.url)
        web_driver.initialize()
        self.driver = web_driver.get_driver()

    def scraper(self, export_file_path: str):
        page_number = 12 
        try:
            csv_file = open(
                export_file_path, "w", encoding="utf-8-sig", newline=""
                )
        except OSError as err:
            logger.warning(err)
        else:
            # if page changes, 버튼을 클릭하면서 data parsing을 합니다. 
            if self.page_change: 
                try:
                    for count in range(page_number):
                        logger.debug(f"PAGE NUMBER: {count}")
                        Parser(self.driver,
                            csv_file,
                            self.fieldnames,
                            self.parent,
                            self.child,
                            self.selectors,).parse_single()
                        # 페이지 넘어갈때마다 button을 한번만 클릭합니다. 
                        # for single click, we pass page_number as -1, not for multiple clicks
                        if self.button_click(
                            self.button_selector, 
                            -1):
                            continue
                        # button_click 함수의 return value가 False면 "Page reaches the end" 의 뜻입니다. loop에서 break합니다 
                        else:
                            break 
                except ValueError as err:
                    logger.warning(err)
                else:
                    logger.info("finished parsing data.")
            # 웹페이지가 next button 형식이 아닌 load more 형식이면 
            # 클릭을 먼저 다 한 다음 data parsing을 진행합니다. 
            else: 
                # 여기선 button을 여러번 클릭합니다. click the button 'count' times
                self.button_click(
                    self.button_selector, 
                    page_number
                    )
                # parsing data
                try:
                    Parser(self.driver,
                            csv_file,
                            self.fieldnames,
                            self.parent,
                            self.child,
                            self.selectors,).parse_single()
                except ValueError as err:
                    logger.warning(err)
                else:
                    logger.info("finished parsing data.")
        finally:
            csv_file.close()

        self.driver.quit()
        logger.info(f"{self.site_name} scraping finished.")
        return True
    
    def button_click(self, button_selector, page_number):
        if page_number == -1:
            button = Finder(self.driver, button_selector, self.driver).get_element()
            if button == None: 
                logger.info("Page reaches the end")
                return False
            else: 
                self.driver.execute_script("arguments[0].click();", button)
                return True
        else:
            for _ in range(0, page_number):
                logger.info(f"PAGE NUMBER: {_}")
                button = Finder(self.driver, button_selector, self.driver).get_element()
                if button == None: 
                    logger.info("Page reaches the end")
                    return False
                else: 
                    self.driver.execute_script("arguments[0].click();", button)
                    time.sleep(3)
            
            return True
    
    
    
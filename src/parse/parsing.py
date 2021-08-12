import csv
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from loguru import logger
from parse.finder import Finder 

# Parse the data
class Parser: 
    def __init__(self, driver, csv_file, fieldnames, parent, child, selectors, is_dynamic=False, scroll_count=12) -> bool:
        self.driver=driver
        self.csv_file = csv_file
        self.fieldnames=fieldnames
        self.parent = parent 
        self.child = child
        self.selectors = selectors 
        self.is_dynamic= is_dynamic
        self.scroll_count = scroll_count        
        pass
    def parse_single(self): 
        writer = csv.DictWriter(self.csv_file, self.fieldnames)
        writer.writeheader()
        
        content_element = Finder(self.driver, self.parent, self.driver).get_element()
        element_list: List[WebElement] = Finder(
            content_element, self.child, self.driver, is_multiple=True
        ).get_element()
        logger.info(f"grep {len(element_list)} elements")

        for element in element_list:
            element_dict = {}

            for fieldname, selector in zip(self.fieldnames, self.selectors):
                element_dict[fieldname] = Finder(
                    element, selector, self.driver, False, True 
                ).get_element()
            
            writer.writerow(element_dict)
        
    def parse_scroll(self):
        writer = csv.DictWriter(self.csv_file, self.fieldnames)
        writer.writeheader()

        # is_dynamic boolean 변수로 페이지가 동적인 selector를 pass 하고 있는지 판단합니다
        # 동적인 selector일때는 scroll 한번 할때마다 list element를 가져와 줘야합니다.
        if self.is_dynamic:
            for count in range(self.scroll_count):
                '''
                parent+ str(count+1) 은 주어진 parent에 1,2,3,4.. 를 추가해줌으로 스크롤 할때마다
                해당 스크롤된 content_element를 가져올 수 있게 만들었습니다.
                '''
                content_element = Finder(self.driver, self.parent + str(count + 1), self.driver).get_element()

                element_list: List[WebElement] = Finder(
                    content_element, self.child, self.driver, is_multiple=True
                    ).get_element()

                logger.info(f"grep {len(element_list)} elements")

                # 여기서 웹페이지에서 찾은 필요한 element들을 csv file로 파싱해줍니다.
                for element in element_list:
                    self.scroll_into_view(self.driver, element)
                    element_dict = {}

                    for fieldname, selector in zip(self.fieldnames, self.selectors):
                        element_dict[fieldname] = Finder(
                        element, selector, self.driver, False, True 
                        ).get_element()
                    writer.writerow(element_dict)
        # 웹페이지가 동적인 selector가 없을때는 스크롤을 count에 맞춰 먼저 하고
        # 그다음 list들을 한꺼번에 가져옵니다
        else:
            content_element = Finder(self.driver, self.parent, self.driver).get_element()
            element_list: List[WebElement] = Finder(
            content_element, self.child, self.driver, is_multiple=True
            ).get_element()
            logger.info(f"grep {len(element_list)} elements")

            for element in element_list:
                self.scroll_into_view(self.driver, element)
                element_dict = {}

                for fieldname, selector in zip(self.fieldnames, self.selectors):
                    element_dict[fieldname] = Finder(
                        element, selector, self.driver, False, True 
                        ).get_element()
                writer.writerow(element_dict)

    def scroll_into_view(self, driver, element):
        """
        scroll_into_view 함수 입니다.
        """
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.implicitly_wait(1)

        return True

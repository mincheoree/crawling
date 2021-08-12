
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from loguru import logger

class Finder: 
    def __init__(self, parent, selector, driver, is_multiple:bool =False, is_text: bool =False) -> None:
        self.parent = parent
        self.selector = selector 
        self.driver = driver
        self.is_multiple = is_multiple
        self.is_text = is_text
        pass

    def find_with_id(self, parent, selector): 
        try:
            WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, selector[1:]))
                )
        except TimeoutException:
            logger.info("Timeout")
            element=None
        else:
            try:
                element = parent.find_element_by_id(selector[1:])
            except NoSuchElementException: 
                logger.debug(f"No such element")
                element=None
                
        return element

    def find_with_tag_name(self, parent, selector):
        try: 
            WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, selector))
                )
        except TimeoutException:
            logger.debug(f"Timeout")
            element= None
        else: 
            try:
                element = parent.find_element_by_tag_name(selector)           
            except NoSuchElementException:
                logger.info("No such element")
                element=None

        return element
    
    def find_with_css_selector(self, parent, selector):
        try: 
            WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
        except TimeoutException:
            logger.debug(f"Timeout")
            element= None
        else: 
            try:
                element = parent.find_element_by_css_selector(selector)           
            except NoSuchElementException:
                logger.info("No such element")
                element=None
            
        return element

    # return list of elements
    def finds_with_css_selector(self, parent, selector):
        try: 
            WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
        except TimeoutException:
            logger.info("Timeout")
            elements=None
        else:
            try:        
                elements = parent.find_elements_by_css_selector(selector)
            except NoSuchElementException: 
                logger.debug(f"No such element")
                elements=None

        return elements
    
    def find_with_link_text(self, parent, selector): 
        try:
            WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, selector))
                )
        except TimeoutException:
            logger.info("Timeout")
            element=None
        else: 
            try:
                element = parent.find_element_by_link_text(selector)       
            except NoSuchElementException: 
                logger.debug(f"No such element")
                element=None
               
        return element 
    
    def find_with_xpath(self, selector):
        try:
            WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, selector))
                )
        except TimeoutException:
            logger.info("Timeout")
            element=None
        else:
            try:  
                element = self.driver.find_element_by_xpath(selector)
            except NoSuchElementException: 
                logger.debug(f"No such element")
                element=None
              
        return element 
    
    def find_with_css_selector_list(self, parent, selector):
        try:
            index = selector[0]
            element: WebElement = parent.find_elements_by_css_selector(selector[1:])[int(index)]
        except NoSuchElementException: 
            logger.debug("No such element")
            element=None

        return element

    def find_with_all(self): 
        if self.selector[0] == "/":
                element = self.find_with_xpath(self.selector)
        elif self.selector[0] == "#":
            element = self.find_with_id(self.parent, self.selector)
        elif self.selector[0] == ".": 
            element = self.find_with_css_selector(self.parent, self.selector)
        elif self.selector[-1] == "*":
            element = self.find_with_css_selector_list(self.parent, self.selector)
        else: 
            element = self.find_with_css_selector(self.parent, self.selector)
            if element == None:
                element = self.find_with_link_text(self.parent, self.selector)
                if element == None: 
                    element = self.find_with_tag_name(self.parent, self.selector)

        return element

    def get_element(self):
        if self.is_multiple:
            element = self.finds_with_css_selector(self.parent, self.selector)
        else:
            if self.is_text:
                element = self.find_with_all()
                if element ==None: 
                    element=""
                else: 
                    element=element.text 
            else: 
                element = self.find_with_all()
        return element




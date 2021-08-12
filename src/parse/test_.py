import pytest
import os
import csv, time
from selenium import webdriver 
from parse.get_driver import Driver 
from parse.finder import Finder
from parse.parsing import Parser
from parse.crawling import Crawler, scroll_to_target_count

# # unit test for testing driver
# @pytest.mark.parametrize("url", ("https://www.openfit.com/search/orange/", "https://www.reddit.com/", "https://www.chosun.com/search/query=corona&siteid=&sort=1&date_period=&writer=&field=&emd_word=&expt_word=&opt_chk=false/"))
# def test_get_driver(url): 
#     print("driver test starts")
#     web_driver = Driver(url)
#     web_driver.initialize()
#     driver = web_driver.get_driver()
#     assert driver, "driver test failed"
#     # assert 0, "test failed"


url = ["https://www.openfit.com/search/orange/"]

# unit test for testing finder
@pytest.fixture(scope="function", params=url)
def f(request):
    web_driver = Driver(request.param)
    web_driver.initialize()
    driver = web_driver.get_driver()
    yield driver


# @pytest.mark.parametrize("selector", ["#tiles-page-1"])
# def test_finder(selector, f): 
#     print("finder test starts")
#     driver = f
#     time.sleep(5)
#     web_element = Finder(driver, selector, driver).get_element()
#     assert web_element, "Cannot find the element"


# def test_scroll(f):
#     print("scroller test starts")
#     scroll_to_target_count(f,
#                             5,
#                             "#tiles-page-",
#                             True,
#                             ".tile"
#                             )

#     element_list: List[WebElement] = f.find_elements_by_css_selector(".tile")
#     assert len(element_list) == 90, "Scrolling failed!"


def test_parse(f):
    print("parser test starts")
    file =open(
                "../export/orange.csv", "w", encoding="utf-8-sig", newline="")
    p = Parser(f,
     csv_file = file, 
     fieldnames=["category", "content"],
     parent="#tiles-page-1",
     child=".tile",
     selectors=[".tile__category", ".tile__title"],)

    p.parse_scroll()
    file = csv.reader("../export/orange/csv")
    row_count = sum(1 for row in file)
    assert row_count > 10, "Failed at Parsing"


    # no method calling

    assert p, "Failed at Parsing"

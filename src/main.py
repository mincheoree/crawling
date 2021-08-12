from parse.buttons.udemy import scraper as udemy_scraper
from parse.buttons.petition import scraper as petition_scraper
from parse.buttons.league import scraper as league_scraper
from parse.buttons.cnn import scraper as cnn_scraper
from parse.buttons.donga import scraper as donga_scraper
from parse.buttons.ruli import scraper as ruli_scraper
from parse.buttons.musinsa import scraper as musinsa_scraper

from parse.crawling import Crawler
from parse.load_more import More 

if __name__ == "__main__":
    # chromedriver_path = "../resources/chromedriver"
    ###multiple buttons


    # udemy_scraper(chromedriver_path, "../export/udemy.csv")
    # petition_scraper(chromedriver_path, "../export/petitions.csv")
    # league_scraper(chromedriver_path, "../export/league.csv")
    # cnn_scraper(chromedriver_path, "../export/cnn.csv")
    # donga_scraper(chromedriver_path, "../export/donga.csv")
    # ruli_scraper(chromedriver_path, "../export/ruli.csv")
    # musinsa_scraper(chromedriver_path, "../export/musinsa.csv")

    ####single button

    # opgg_scraper(chromedriver_path, "../export/opgg.csv")
    # ft_scraper(chromedriver_path, "../export/ft.csv")
    # chosun_scraper(chromedriver_path, "../export/chosun.csv")
    # daum_scraper(chromedriver_path, "../export/daum.csv")

    #### scrolling
    # reddit_scraper(chromedriver_path, "../export/reddit.csv")
    # orange_scraper(chromedriver_path, "../export/orange.csv")
    # idus_scraper(chromedriver_path, "../export/idus.csv")
    # pin_scraper(chromedriver_path, "../export/pin.csv")

    # Crawler(
    #     url="https://www.idus.com/w/main/category/613ac4c3-df73-4a0f-b3dd-362849dabb2a",
    #     fieldnames=[
    #         "category",
    #         "name",
    #         "sale rate",
    #         "sale price",
    #         "rating",
    #     ],
    #     selectors=[
    #         ".product-info__artist-name",
    #         ".product-info__name",
    #         ".sale-rate",
    #         ".price-sale",
    #         ".review-count",
    #     ],
    #     parent='//*[@id="content"]/div[2]/div/div',
    #     is_dynamic=False,
    #     child=".ui_grid__item",
    #     site_name="idus",
    # ).scraper(export_file_path="../export/idus.csv")

    # Crawler(
    #     url="https://www.pinterest.co.kr/dogs/",
    #     fieldnames=["topic", "content"],
    #     selectors=["figcaption", ".hDW"],
    #     parent=".Collection",
    #     is_dynamic=False,
    #     child=".Collection-Item",
    #     site_name="pinterest",
    #     backup_selectors=[".tBJ", ".ujU"],
    #     backup_parent=".mobileGrid",
    #     backup_child=".Yl-"
    # ).scraper(export_file_path="../export/pin.csv")

    
    # Crawler(
    #     url="https://www.reddit.com/",
    #     fieldnames=["vote", "author", "content"],
    #     selectors=[
    #         "._1rZYMD_4xY3gRcSS3p8ODO",
    #         "._3AStxql1mQsrZuUIFP9xSg",
    #         ".y8HYJ-y_lTUHkQIc1mdCq",
    #     ],
    #     parent='//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[5]',
    #     is_dynamic=False,
    #     child=".scrollerItem",
    #     site_name="reddit",
    # ).scraper(export_file_path="../export/reddit.csv")

    # Crawler(
    #     url="https://www.openfit.com/search/orange/",
    #     fieldnames=["category", "content"],
    #     selectors=[".tile__category", ".tile__title"],
    #     parent="#tiles-page-",
    #     is_dynamic=True,
    #     child=".tile",
    #     site_name="openfit",
    # ).scraper(export_file_path="../export/orange.csv")

    # More(
    #     url= "https://www.chosun.com/search/query=corona&siteid=&sort=1&date_period=&writer=&field=&emd_word=&expt_word=&opt_chk=false/",
    #     fieldnames= ["headline", "content", "category", "author", "date"],
    #     selectors = [".story-card__headline-container", ".story-card__deck",  "0div.story-card__breadcrumb > *",  "1div.story-card__breadcrumb > *",  "2div.story-card__breadcrumb > *"],
    #     parent = '//*[@id="main"]/div[2]',
    #     child = ".story-card-wrapper",
    #     page_change= False,
    #     button_selector= "#load-more-stories",
    #     site_name = "chosun",
    # ).scraper(export_file_path="../export/chosun.csv")

    # More(
    #     url= "https://sports.daum.net/news/breaking/#313539383934353937313137355e2a7c2c232d404174586463584e7a6768",
    #     fieldnames= ["title", "content", "category", "time", "publisher"],
    #     selectors = [".tit_news", ".link_desc", "0span.info_news > *", "1span.info_news > *", "2span.info_news > *"],
    #     parent = '//*[@id="newsData"]/ul',
    #     child = ".wrap_cont",
    #     page_change= False,
    #     button_selector= ".link_moreview",
    #     site_name = "daum",
    # ).scraper(export_file_path="../export/daum.csv")

    # More(
    #     url= "https://www.ft.com/world",
    #     fieldnames= ["date", "category", "heading", "content"],
    #     selectors = [".stream-card__date", ".o-teaser__meta", ".o-teaser__heading", ".o-teaser__standfirst"],
    #     parent = '//*[@id="stream"]/div[1]/ul',
    #     child = ".o-grid-row",
    #     page_change= True,
    #     button_selector= ".o-buttons-icon--arrow-right",
    #     site_name = "financial times",
    # ).scraper(export_file_path="../export/ft.csv")
    
    # More(
    #     url= "https://talk.op.gg/s/lol/opgg",
    #     fieldnames= ["votes", "title", "date", "author"],
    #     selectors = [".article-list-item__vote", ".article-list-item__title", "0div.article-list-item-meta > *", "1div.article-list-item-meta > *"],
    #     parent = '//*[@id="content"]/section[2]',
    #     child = ".article-list-item",
    #     page_change= True,
    #     button_selector= "다음",
    #     site_name = "opgg",
    # ).scraper(export_file_path="../export/opgg.csv")
    pass


import os
import re
import config
from app.run import RunClass
from app.scrap_all import scrap_all
from app.scrap_each import scrap_each
from app.search import NYSearch
from utils.directory import directory
from infra.driver import driver
from infra.download_image import downloads
from infra.logging_config import log_info, log_warning
from domain.save_data import save
from domain.money import moneychecker
from domain.phrase_count import phrase_counter
from robocorp.tasks import task

# class RunClass:
#     def __init__(self, driver, query, subject):
#         self.driver = driver
#         self.query = query
#         self.subject = subject
#         self.excel_path = os.path.join("output", "news.xlsx")
#         self.images_path = os.path.join("output")
#         self.save_path = None

#         self.search = NYSearch(driver, self.query, self.subject)
#         self.directory = directory(self.query)
#         self.scrap_all = scrap_all(self.driver)
#         self.scrap_each = scrap_each(self.driver)
#         self.downloads = downloads()
#         self.save = save(self.excel_path)

#     def run_search(self):
#         log_info("Starting the automation.")

#         # Start the search
#         self.search.search()

#         # Scrape all list items
#         log_info("Compiling list of news articles...")
#         list_items = self.scrap_all.scrape_list_items()
        
#         log_info("Beginning detailed information scraping for each news item.")
#         try:
#             for item in list_items:
#                 # Scrape details for each item
#                 data = self.scrap_each.scrape_item_details(item)
#                 if data:
#                     for url in data["imageUrls"]:
#                         filename = f'{data["newsData"]["headings"]}.jpg'
#                         filename = re.sub(r'[\\/:*?"<>|\[\]]', "", filename)
#                         self.save_path = os.path.join(self.images_path, filename)
#                         downloads.download_image(url, self.save_path)
#                     data["newsData"]["savePath"] = self.save_path
#                     data["newsData"]["containsMoney"] = moneychecker.check_data_for_money(data)
#                     data["newsData"]["phraseCounter"] = phrase_counter.count_query_in_data(data, self.query)
#                     self.save.save_to_xlsx(data)
#         finally:
#             log_info(f"Data secured at excel file - news.xlsx") 

#         log_info("Automation completed successfully.")      
#         self.driver.quit()
#         return []

driver_class = driver()
driver1 = driver_class.set_webdriver()
ny_search = RunClass(driver1, config.query, config.subject)

@task
def run_task():
    ny_search.run_search()

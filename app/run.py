import logging
import config
import re 
import os
from rpaChallenge.utils.directory import directory
from rpaChallenge.infra.download_image import downloads
from rpaChallenge.domain.save_data import save
from rpaChallenge.domain.money import moneychecker
from rpaChallenge.domain.phrase_count import phrase_counter
from rpaChallenge.app.scrap_all import scrap_all
from rpaChallenge.app.scrap_each import scrap_each
from rpaChallenge.app.search import NYSearch
from robocorp.tasks import task


class RunClass:
    def __init__(self, driver, query, subject):
        self.logger = logging.getLogger(__name__)
        self.driver = driver
        self.query = query
        self.subject = subject

        self.file_path = f"{config.path}\\{self.query}"
        self.file_path = self.file_path.replace(" ","_")
        self.excel_path = os.path.join(self.file_path, "news.xlsx")
        self.images_path = os.path.join(self.file_path, "images")
        self.save_path = None

        self.search = NYSearch(self.driver, self.query, self.subject)
        self.directory = directory(self.query)
        self.scrap_all = scrap_all(self.driver)
        self.scrap_each = scrap_each(self.driver)
        self.downloads = downloads()
        self.save = save(self.excel_path)

    @task
    def run_search(self):
        self.logger.info("Starting the automation.")

        # Create directory
        self.logger.info("Creating directories...")
        self.directory.create_directory()
        
        # Start the search
        self.search.search()

        # Scrape all list items
        self.logger.info("Compiling list of news articles...")
        list_items = self.scrap_all.scrape_list_items()
        
        self.logger.info("Beginning detailed information scraping for each news item.")
        try:
            for item in list_items:
                # Scrape details for each item
                data = self.scrap_each.scrape_item_details(item)
                if data:
                    for url in data["imageUrls"]:
                        filename = f'{data["newsData"]["headings"]}.jpg'
                        filename = re.sub(r'[\\/:*?"<>|\[\]]', "", filename)
                        self.save_path = os.path.join(self.images_path, filename)
                        downloads.download_image(url, self.save_path)
                    data["newsData"]["savePath"] = self.save_path
                    data["newsData"]["containsMoney"] = moneychecker.check_data_for_money(data)
                    data["newsData"]["phraseCounter"] = phrase_counter.count_query_in_data(data, self.query)
                    self.save.save_to_xlsx(data)
        finally:
            self.logger.info(f"Data secured at excel file - news.xlsx") 
                
        self.logger.info("Automation completed successfully.")      
        self.driver.quit()
        return []
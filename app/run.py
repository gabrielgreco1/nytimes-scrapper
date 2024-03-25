import logging
import config
import re 
import os
from utils.directory import directory
from app.scrap_all import scrap_all
from app.scrap_each import scrap_each
from infra.download_image import downloads
from domain.save_data import save
from app.search import NYSearch


class run:
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

    def run_search(self):
        self.logger.info('Starting the automation')

        # Create directory
        self.logger.info('Creating directorys...')
        self.directory.create_directory()
        
        # Start the search
        self.logger.info('Searching news for the required parameters')
        self.search.search()

        # Scrape all list items
        self.logger.info('Listing all news...')
        list_items = self.scrap_all.scrape_list_items()
        
        self.logger.info('Starting to scrap all the information from each item')
        for item in list_items:
            # Scrape details for each item
            data = self.scrap_each.scrape_item_details(item)
            if data:
                for index, url in enumerate(data["imageUrls"]):
                    filename = f"{data['newsData']['headings']}.jpg"
                    filename = re.sub(r'[\\/:*?"<>|\[\]]', "", filename)
                    self.save_path = os.path.join(self.images_path, filename)
                    downloads.download_image(url, self.save_path)
                data['newsData']['savePath'] = self.save_path
                self.save.save_to_xlsx(data)
                
        self.logger.info('Automation Finished')      
        self.driver.quit()
        return []
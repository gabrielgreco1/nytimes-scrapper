from selenium.webdriver.common.by import By

class scrap_each:
    def __init__(self, driver):
        self.driver = driver
        self.newsData = {}
        self.title = None
        self.date = None
        self.description = None
        self.links = None
        self.imagesUrls = None


    def scrape_item_details(self, list_item):
        
        # Extract headings
        self.title = [heading.text for heading in list_item.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")]

        # Extract <span> element
        self.date = [span.text for span in list_item.find_elements(By.CSS_SELECTOR, "span")]

        # Extract <p> elements
        self.description = [p.text for p in list_item.find_elements(By.CSS_SELECTOR, "p")]

        # Extract <a> elements
        self.links = [a.get_attribute("href") for a in list_item.find_elements(By.CSS_SELECTOR, "a")]

        # Extract <img> inside <figure>
        figures = list_item.find_elements(By.CSS_SELECTOR, "div > figure")
        self.imagesUrls = [fig.find_element(By.TAG_NAME, "img").get_attribute("src") for fig in figures if fig.find_element(By.TAG_NAME, "img")]

        # Insert data into the object
        self.newsData["headings"] = self.title
        self.newsData["date"] = self.date
        self.newsData["paragraphs"] = self.description
        self.newsData["links"] = self.links


        # Returning a Dict with the scrapped info 
        return {
            "newsData": self.newsData,
            "imageUrls": self.imagesUrls
        }
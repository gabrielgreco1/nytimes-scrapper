from selenium.webdriver.common.by import By

class scrap_each:
    def __init__(self, driver):
        self.driver = driver
        self.title = None
        self.date = None
        self.description = None


    def scrape_item_details(self, list_item):
        
        newsData = {}

        # Extract headings
        self.title = [heading.text for heading in list_item.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")]
        newsData["headings"] = self.title

        # Extract <span> element
        self.date = [span.text for span in list_item.find_elements(By.CSS_SELECTOR, "span")]
        newsData["date"] = self.date

        # Extract <p> elements
        self.title = [p.text for p in list_item.find_elements(By.CSS_SELECTOR, "p")]
        newsData["paragraphs"] = self.title

        # Extract <a> elements
        newsData["links"] = [a.get_attribute("href") for a in list_item.find_elements(By.CSS_SELECTOR, "a")]

        # Extract <img> inside <figure>
        figures = list_item.find_elements(By.CSS_SELECTOR, "div > figure")
        imagesUrls = [fig.find_element(By.TAG_NAME, "img").get_attribute("src") for fig in figures if fig.find_element(By.TAG_NAME, "img")]

        # Returning a Dict with the scrapped info 
        return {
            "newsData": newsData,
            "imageUrls": imagesUrls
        }
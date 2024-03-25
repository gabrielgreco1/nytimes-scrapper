from search import NYSearch
from driver import driverSettings
import config

if __name__ == "__main__":
    driver = driverSettings()
    nyt_search = NYSearch(driver, config.query, config.subject, config.months)
    results = nyt_search.run()
    # for result in results:
    #     print(result)
    # nyt_search.driver.quit()
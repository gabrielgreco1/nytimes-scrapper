from search import NYSearch
from infra.driver import driverSettings
import config

if __name__ == "__main__":
    driver = driverSettings()
    ny_search = NYSearch(driver, config.query, config.subject, config.months)
    results = ny_search.run()
    # for result in results:
    #     print(result)
    # nyt_search.driver.quit()
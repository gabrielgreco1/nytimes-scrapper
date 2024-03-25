from app.run import run
from infra.driver import driverSettings
import config

if __name__ == "__main__":
    driver = driverSettings()
    ny_search = run(driver, config.query, config.subject)
    ny_search.run_search()

from infra.logging_config import setup_logging
from robocorp.tasks import task
setup_logging()

from app.run import RunClass
from infra.driver import driverSettings
import config

@task
def run_task():
    driver = driverSettings()
    ny_search = RunClass(driver, config.query, config.subject)
    ny_search.run_search()

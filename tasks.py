from robocorp.tasks import task
from app.run import RunClass
from infra.driver import driver
import config
driver_class = driver()
driver1 = driver_class.set_webdriver()
ny_search = RunClass(driver1, config.query, config.subject)
@task
def run_task():
    ny_search.run_search()

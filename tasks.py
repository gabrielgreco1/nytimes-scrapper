from app.run import RunClass
from infra.driver import driver
from robocorp.tasks import task
from robocorp import workitems

driver_class = driver()
driver1 = driver_class.set_webdriver()

@task
def run_task():
    item = workitems.inputs.current  # This assigns the current input item to 'item'

    # Checks if the 'query' key is in the current item's payload
    if 'query' in item.payload:
        query = item.payload['query']

    if 'subject' in item.payload:
        subject = item.payload['subject']
    else:
        subject = 'Any'

    if 'months' in item.payload:
        months = item.payload['months']
    
    # Continue with the output creation
    workitems.outputs.create(payload={"key": "value"})
    ny_search = RunClass(driver1, query, subject, months)
    ny_search.run_search()
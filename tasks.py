from app.run import RunClass
from infra.driver import driver
from robocorp.tasks import task
from robocorp import workitems
import config

driver_class = driver()
driver1 = driver_class.set_webdriver()

@task
def run_task():
    item = workitems.inputs.current  # Isso atribui o item de entrada atual a 'item'
    print("Received payload:", item.payload)

    # Verifica se a chave 'query' está no payload do item atual
    if 'query' in item.payload:
        query = item.payload['query']
        print('...................................', query)
    if 'subject' in item.payload:
        subject = item.payload['subject']
        print('...................................', subject)
    
    # Continua com a criação do output
    workitems.outputs.create(payload={"key": "value"})
    ny_search = RunClass(driver1, query, subject)
    ny_search.run_search()


# def workitems():
#     for item in workitems.inputs:
#         print("Received payload:", item.payload)
    
#         # Verifica se a chave 'query' existe no payload
#         if 'query' in item.payload:
#             query = item.payload['query']
#             print("A query é:", query)
    
#         # Seu código existente para criar outputs
#         workitems.outputs.create(payload={"key": "value"})


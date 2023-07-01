from fastapi import FastAPI

from docguptea.utils import DBConnection

app = FastAPI(title="DocGup-Tea",
              version="V0.0.1",
              description="API for automatic documentation generation!"
              )

from docguptea import router

try:
    dbconnection = DBConnection()
    print(f"Connection successful:{dbconnection.get_client()}")
except Exception as e:
    print(e)

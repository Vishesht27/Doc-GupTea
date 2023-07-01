import pyodbc

# fix ObjectId & FastApi conflict
import pydantic
from bson.objectid import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

from typing import Union, Tuple, List

from docguptea.utils import DBConnection
from docguptea.core.Exceptions import *


class DBQueries:
    @classmethod
    def insert_to_database(cls, coll_name:str, data:Union[Tuple, List[Tuple]]):
        con = DBConnection.get_client()
        cursor = con.cursor()
        QUERY = ('INSERT INTO {coll_name} '
                 '(username, password, email) '
                 'VALUES '
                 '(%s, %s, %s)').format(coll_name=coll_name)

        if isinstance(data, List[Tuple]):
            return cursor.executemany(QUERY, data)
        else:
            return cursor.execute(QUERY, data)
from q1 import create_engine

from sqlalchemy import MetaData , Table , Column , Row , Integer , String , CheckConstraint
from q1 import engine

metadata = MetaData()

students_table = Table(
    "students_table" ,
    metadata,
    Column ("id", Integer , primary_key=True ),
    Column ("name", String , nullable= False),
    Column ("age", Integer,),
    Column ("city", String, nullable= True ),
    CheckConstraint ("age>= 18" )
)

def create_tables():
    metadata.create_all(engine)

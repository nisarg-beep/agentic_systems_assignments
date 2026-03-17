from q1 import engine
from tables import students_table
from sqlalchemy import insert , select , update , delete

def create_student_data(input_name , input_age , input_city ):
    with engine.connect() as conn:
        query = insert(students_table).values(name = input_name, age= input_age, city = input_city)
        conn.execute(query)
        conn.commit()


def get_all_students_data():
    with engine.connect() as conn:
        query = select(students_table)
        data = conn.execute(query).fetchall()
        return data
    
def update_students_data(input_student_name, input_student_city):
    with engine.connect() as conn:
        query = update (students_table).where(students_table.c.name == input_student_name).values(city= input_student_city)
        conn.execute(query)
        conn.commit ()

def delete_student():
    with engine.connect() as conn:
        query = delete(students_table).where(students_table.c.age < 20)
        conn.execute(query) 
        conn.commit()
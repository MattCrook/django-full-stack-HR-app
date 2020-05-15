import sqlite3
from hrapp.views.connection import Connection
from hrapp.models import model_factory, Employee

def get_all_employees():
    """
    This function gets all of the employee data from hrapp_employee
    """
    with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Employee)
            db_cursor = conn.cursor()

            '''
            Joins employee table with department table
            returns
            - Employee Id
            - Employee First Name
            - Employee Last Name
            - Employee Start Date
            - Employee is supervisor
            - Employee Department
            '''

            # Got rid of join

            db_cursor.execute("""
                SELECT
                    *
                FROM
                    hrapp_employee e
            """)

            return db_cursor.fetchall()
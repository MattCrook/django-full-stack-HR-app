import sqlite3
from hrapp.views.connection import Connection
from hrapp.models import model_factory, Employee
def get_employee(employee_id):
    """
    This function gets all of the data for onw user from hrapp_employee
    """
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)

        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            *
        FROM
            hrapp_employee e
        WHERE
            e.id = ?
        """, (employee_id, ))

        dataset = db_cursor.fetchone()

        return dataset



import sqlite3
from hrapp.views.connection import Connection
from hrapp.models import model_factory, Department

def get_all_departments():
    """
    This function gets all of the department data from hrapp_department
    """
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                *
            FROM
                hrapp_department
        """)

        return db_cursor.fetchall()
import sqlite3
# from ....connection import Connection
from hrapp.views.connection import Connection
from hrapp.models import model_factory, TrainingProgram

def get_all_trainings():
    """
    This function gets all of the department data from hrapp_department
    """
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgram)
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                *
            FROM
                hrapp_trainingprogram
        """)

        return db_cursor.fetchall()
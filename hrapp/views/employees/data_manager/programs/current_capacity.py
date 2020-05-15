import sqlite3
from hrapp.views.connection import Connection
from hrapp.models import model_factory, TrainingProgramEmployee
def current_capacity(program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgramEmployee)

        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            Count(*) count
        FROM
            hrapp_trainingprogramemployee tre
        WHERE
            tre.training_program_id = ?
        GROUP BY training_program_id
        """, (program_id, ))

        data = db_cursor.fetchone()
        return_this = data.count if hasattr(data, "count") else 0
        
        return return_this
import sqlite3
from hrapp.views.connection import Connection
import datetime


def assign_program(employee_id, program_id):
    if program_id:
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_trainingprogramemployee (training_program_id, employee_id)
            VALUES(?, ?)
            """, (program_id, employee_id))
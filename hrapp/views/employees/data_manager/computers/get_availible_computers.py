import sqlite3
from hrapp.views.connection import Connection
from hrapp.models import model_factory, EmployeeComputer, Computer


def get_availible_computers():
    """
    This function grabs all computers that are not assigned to an employee
    """
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            *
        FROM
            hrapp_computer ec
        """)

        dataset = db_cursor.fetchall()
        computer_dict = dict()

        for row in dataset:
            computer_dict[row.id] = row

        new_dataset = []

        conn.row_factory = model_factory(EmployeeComputer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            *
        FROM
            hrapp_employeecomputer ec
        """)

        dataset = db_cursor.fetchall()

        for row in dataset:
            computer_dict[row.computer_id] = row

        new_dataset = []
        for id, relationship in computer_dict.items():
            if hasattr(relationship, "unassign_date"):
                if relationship.unassign_date:
                    new_dataset.append(computer_dict[id].computer)
            else:
                new_dataset.append(computer_dict[id])

        return new_dataset

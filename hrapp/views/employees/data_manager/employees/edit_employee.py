import sqlite3
from hrapp.views.connection import Connection
import datetime


def edit_employee(form_data, employee_id):
    """
    This function edits an employee to the hrapp_employee table
    This function edits an employee_computer relationship to the hrapp_employeecomputer table
    """
    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()

        if form_data["computer"] != form_data["computer_owned"]:
            now = datetime.datetime.now()
            assigned_date = now.strftime("%Y-%m-%d")
            if form_data["computer"] == "":
                db_cursor.execute("""
                    UPDATE hrapp_employeecomputer
                    SET unassign_date = ?
                    WHERE hrapp_employeecomputer.id = ?
                    """, (assigned_date, form_data["computer_relationship"]))
            else:

                if form_data["computer_owned"] != "":
                    db_cursor.execute("""
                    UPDATE hrapp_employeecomputer
                    SET unassign_date = ?
                    WHERE hrapp_employeecomputer.id = ?
                    """, (assigned_date, form_data["computer_relationship"]))

                db_cursor.execute("""
                Insert into hrapp_employeecomputer (computer_id, employee_id, assign_date)
                Values (?, ?, ?)
                """, (form_data["computer"], employee_id, assigned_date))

        # Updated Employee information
        db_cursor.execute("""
        UPDATE hrapp_employee
        SET
            last_name = ?,
            department_id = ?
        WHERE hrapp_employee.id = ?;
        """, (
            form_data["last_name"],
            form_data["department"],
            employee_id
        ))

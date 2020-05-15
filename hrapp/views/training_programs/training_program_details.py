import sqlite3
import datetime
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from hrapp.models import TrainingProgram, Employee, TrainingProgramEmployee
from hrapp.models import model_factory
from ..connection import Connection


def create_training_program(cursor, row):
    _row = sqlite3.Row(cursor, row)

    training_program = TrainingProgram()
    training_program.id = _row["id"]
    training_program.title = _row["title"]
    training_program.start_date = _row["start_date"]
    training_program.end_date = _row["end_date"]
    training_program.capacity = _row["capacity"]

    training_program_employee = TrainingProgramEmployee()
    training_program_employee.id = _row["id"]
    training_program_employee.employee_id = _row["employee_id"]
    training_program_employee.training_program_id = _row["training_program_id"]

    employee = Employee()
    employee.id = _row["employee_id"]
    employee.first_name = _row["first_name"]
    employee.last_name = _row["last_name"]
    employee.start_date = _row["start_date"]

    training_program.employee = employee
    training_program.training_program_employee = training_program_employee
    return training_program


def get_training_program(training_program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_training_program
        db_cursor = conn.cursor()

        db_cursor.execute("""
           SELECT
             tp.id,
             tp.title,
             tp.start_date,
             tp.end_date,
             tp.capacity,
             e.id,
             e.first_name,
             e.last_name,
             e.start_date,
             etp.id,
             etp.employee_id,
             etp.training_program_id
         FROM hrapp_trainingprogram tp
         LEFT JOIN hrapp_trainingprogramemployee etp ON etp.training_program_id = tp.id
         LEFT JOIN hrapp_employee e ON etp.employee_id = e.id
        WHERE tp.id = ?
        """, (training_program_id,))
        return db_cursor.fetchone()


def get_count(training_program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
                SELECT COUNT(training_program_id)
                FROM hrapp_trainingprogramemployee
                WHERE training_program_id = ?
            """, (training_program_id, ))
        return db_cursor.fetchone()


@login_required
def training_program_details(request, training_program_id):
    if request.method == 'GET':
        training_program = get_training_program(training_program_id)
        current_date = datetime.date.today()
        start_date_program = datetime.datetime.strptime(training_program.start_date,
                                                        '%Y-%m-%d').date()
        count = get_count(training_program_id)
        template = 'training_programs/training_program_details.html'
        context = {
            "training_program": training_program,
            "start_date_program": start_date_program,
            "current_date": current_date,
            "get_count": count[0]
        }
        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                db_cursor.execute("""
                    UPDATE hrapp_trainingprogram
                    SET title = ?,
                        start_date = ?,
                        end_date = ?,
                        capacity = ?
                    WHERE id = ?
                """,
                                  (form_data['title'], form_data['start_date'], form_data['end_date'],
                                   form_data['capacity'], training_program_id,))

            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                db_cursor.execute("""
                    INSERT INTO hrapp_trainingprogramemployee
                    (employee_id, training_program_id)
                    VALUES (?, ?)
                    """,
                                  (form_data['employee_id'], training_program_id,))
            return redirect(reverse('hrapp:trainingprograms'))

        if (
            "actual_method" in form_data and form_data["actual_method"] == "DELETE"
        ):
            program_to_be_deleted = get_object_or_404(TrainingProgram,
                                                      pk=training_program_id)

            program_to_be_deleted.delete()

            return redirect(reverse('hrapp:trainingprograms'))

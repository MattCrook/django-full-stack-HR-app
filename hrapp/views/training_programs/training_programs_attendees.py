import sqlite3
from django.shortcuts import render, redirect, reverse
from hrapp.models import TrainingProgram, TrainingProgramEmployee, Employee
from ..connection import Connection
from django.contrib.auth.decorators import login_required
from hrapp.models import model_factory


@login_required
def employee_attendees(request, training_program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgramEmployee)
        db_cursor = conn.cursor()
        db_cursor.execute("""
                    SELECT
                        tp.id,
                        tp.title,
                        tp.start_date,
                        tp.end_date,
                        tp.capacity,
                        e.id employee_id,
                        e.first_name,
                        e.last_name,
                        e.start_date,
                        etp.id,
                        etp.employee_id,
                        etp.training_program_id
                    FROM hrapp_trainingprogramemployee etp
                    JOIN hrapp_trainingprogram tp ON tp.id = etp.training_program_id
                    JOIN hrapp_employee e ON etp.employee_id = e.id
                    WHERE tp.id = ?
                """, (training_program_id, ))
        data = db_cursor.fetchall()

    template_name = 'training_programs/training_programs_attendees.html'
    context = {
        'attendees': data
    }
    return render(request, template_name, context)

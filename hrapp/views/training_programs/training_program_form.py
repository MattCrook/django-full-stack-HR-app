import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from hrapp.models import TrainingProgram, Employee, TrainingProgramEmployee
from hrapp.models import model_factory
from ..connection import Connection
from .training_program_details import get_training_program


def get_training_programs():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgram)
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT
                tp.id,
                tp.title,
                tp.start_date,
                tp.end_date,
                tp.capacity
            FROM hrapp_trainingprogram tp
            """ )
        return db_cursor.fetchall()


def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT
                e.id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor
            FROM hrapp_employee e
            """ )
        return db_cursor.fetchall()


def get_training_program_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgramEmployee)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT *
        FROM hrapp_trainingprogramemployee tpe
        """)
        return db_cursor.fetchall()


@login_required
def training_program_form(request):
    if request.method == 'GET':
        training_programs = get_training_programs()
        template = "training_programs/training_program_form.html"
        context = {
            "training_program": training_programs
        }
        return render(request, template, context)


@login_required
def training_program_edit_form(request, training_program_id):
    if request.method == 'GET':
        training_program = get_training_program(training_program_id)
        employees = get_employees()
        training_program_employees = get_training_program_employees()
        template = "training_programs/training_program_form.html"
        context = {
            "training_program": training_program,
            "employees": employees,
            "training_program_employees": training_program_employees
        }
        return render(request, template, context)

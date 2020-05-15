import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from hrapp.models import Department, Employee
from hrapp.models import model_factory
from ..connection import Connection


def get_employees(department_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
            e.id,
            e.first_name,
            e.last_name,
            e.start_date,
            e.department_id
            FROM hrapp_employee e
            WHERE e.department_id = ?                          
            """, (department_id,))

        dep_employees = []
        data = db_cursor.fetchall()

        for row in data:
            employee = Employee()
            employee.id = row['id']
            employee.first_name = row['first_name']
            employee.last_name = row['last_name']

            dep_employees.append(employee)

        return dep_employees


def get_department(department_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            d.id,
            d.department_name,
            d.budget
        FROM hrapp_department d
        WHERE d.id = ?
        """, (department_id,))

        return db_cursor.fetchone()


@login_required
def department_detail(request, department_id):
    if request.method == 'GET':
        department = get_department(department_id)
        employees = get_employees(department_id)

        template = 'departments/department_details.html'
        context = {
            'department': department,
            'employees': employees
        }

        return render(request, template, context)

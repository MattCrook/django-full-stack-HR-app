import sqlite3
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from hrapp.models import Department, model_factory
from ..connection import Connection



def department_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
          SELECT 
                Count(e.id) employees,
                d.department_name,
                d.id,
                d.budget,
                e.id
            FROM hrapp_department d
            Left JOIN hrapp_employee e ON e.department_id = d.id
            GROUP BY d.department_name
                        """)

            all_departments = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                department = Department()
                department.id = row['id']
                department.department_name = row['department_name']
                department.budget = row['budget']
                department.employees = row['employees']

                all_departments.append(department)

        template = 'departments/departments_list.html'
        context = {
            'departments': all_departments
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST
        
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()
            
            db_cursor.execute("""
            INSERT INTO hrapp_department
            (
                department_name, budget
            )
            VALUES (?, ?)
            """,
            (form_data['department_name'], form_data['budget']))
            
        return redirect(reverse('hrapp:departments'))
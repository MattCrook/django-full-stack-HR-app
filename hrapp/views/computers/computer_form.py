import sqlite3
import datetime
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee, Computer, model_factory, EmployeeComputer
from ..connection import Connection
from django import forms


def get_employees():
    ''' 
        This function is just to fetch all the employees and return it so we can populate a dropdown menu based off it.
    '''
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()
        now = datetime.datetime.now()
        today_date = now.strftime("%Y-%m-%d")

        db_cursor.execute('''
         select 
            e.first_name,
            e.last_name,
            e.id,
            e.is_supervisor
            from hrapp_employee e
        ''')

        employees = db_cursor.fetchall()
        return employees

@login_required
def computer_form(request):
    # this function calls the above function to grab all the employees (so it can populate a dropdown menu) and then sends the user to the right html

    if request.method == "GET":
        employees = get_employees()
        template = 'computers/computer_form.html'
        context = {
            'employees': employees
        }

        return render(request, template, context)

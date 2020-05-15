from django.shortcuts import render
from .data_manager import (
    get_employee_training, 
    get_all_trainings,
    get_all_departments,
    get_employee,
    is_full
)
from datetime import date, datetime

def employee_add_program(request, employee_id):
    """
    This function handles all of the request to the edit employee page
    """
    if request.method == "GET":
        employee = get_employee(employee_id)
        all_programs = get_all_trainings()
        employee_trainings = [i.training_program.title for i in get_employee_training(employee_id)]
        programs = [i for i in all_programs if i.title not in employee_trainings and datetime.strptime(i.start_date, '%Y-%m-%d').date() > date.today()]
        availible_programs = [i for i in programs if is_full(i.id)]

        template = "employees/employee_add_program.html"
        context = {
            "programs": availible_programs,
            "employee": employee
        }
        return render(request, template, context)

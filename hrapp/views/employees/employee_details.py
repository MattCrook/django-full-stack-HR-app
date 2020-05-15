from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .data_manager import (
    get_employee_computers, 
    get_employee_training, 
    assign_program, 
    edit_employee,
    get_employee
)


@login_required
def employee_details(request, employee_id):
    """
    This function handles all of the request to the employee's detail page
    """
    if request.method == "GET":
        employee = get_employee(employee_id)
        employee_computers = get_employee_computers(employee_id)
        employee_programs = [
            i.training_program for i in get_employee_training(employee_id)]
        template = "employees/employee_details.html"

        context = {
            "employee_computers": employee_computers,
            "employee_programs": employee_programs,
            "employee": employee
        }

        return render(request, template, context)
    elif request.method == "POST":
        form_data = request.POST

        if "actual_method" in form_data and form_data["actual_method"] == "PUT":
            edit_employee(form_data, employee_id)
            return redirect("hrapp:employee", employee_id=employee_id)
        elif "actual_method" in form_data and form_data["actual_method"] == "AssignProgram":
            assign_program(employee_id, form_data["program"])
            return redirect("hrapp:employee", employee_id=employee_id)

        
        

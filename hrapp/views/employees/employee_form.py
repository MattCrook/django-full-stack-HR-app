from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .data_manager import (
    get_all_departments,
    get_employee,
    get_employee_computers,
    get_availible_computers
)

@login_required
def employee_add(request):
    """
    This function handles all of the request to the add employee page
    """
    if request.method == "GET":
        departments = get_all_departments()
        template = "employees/employee_form.html"
        context = {
            "departments": departments
        }

        return render(request, template, context)

@login_required
def employee_edit(request, employee_id):
    """
    This function handles all of the request to the edit employee page
    """
    if request.method == "GET":
        employee = get_employee(employee_id)
        departments = get_all_departments()
        computer_owned = get_employee_computers(employee_id)
        computers = get_availible_computers()
        if computer_owned: computers.append(computer_owned.computer)
        template = "employees/employee_form.html"
        context = {
            "employee": employee,
            "departments": departments,
            "computers": computers,
            "computer_owned": computer_owned
        }
        return render(request, template, context)

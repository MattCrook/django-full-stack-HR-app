from django.shortcuts import render, redirect, reverse
from .data_manager import (
    add_employee,
    get_all_employees
)

def employee_list(request):
    """
    This function handles all of the request to the employee list page
    """
    if request.method == 'GET':
        all_employees = get_all_employees()

        template = 'employees/employees_list.html'
        context = {
            'employees': all_employees
        }

        return render(request, template, context)
    elif request.method == "POST":
        form_data = request.POST
        add_employee(form_data)
        return redirect(reverse("hrapp:employee_list"))

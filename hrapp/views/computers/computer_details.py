import sqlite3
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from hrapp.models import model_factory, Computer
from ..connection import Connection


def get_computer(computer_id):
    # connect to the database
    with sqlite3.connect(Connection.db_path) as conn:
        # set row parameters and then set up the database cursor
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()

        # database select
        db_cursor.execute("""
            SELECT c.id,
                c.make,
                c.manufacturer,
                c.purchase_date,
                c.decommission_date,
                ec.assign_date,
                ec.unassign_date,
                e.first_name,
                e.last_name,
                COUNT(e.first_name) count
                from hrapp_computer c
                left join hrapp_employeecomputer ec on ec.computer_id = c.id
                left join hrapp_employee e on ec.employee_id = e.id
                where c.id = ?
        """, (computer_id,))
        # return the results from the fetch call
        data = db_cursor.fetchall()[-1]
        return data


@login_required
def computer_details(request, computer_id):
    if request.method == "GET":
        # fetch that one computer using helper function
        computer = get_computer(computer_id)
        print("first name", computer.first_name)

        template = 'computers/computer_details.html'
        context = {
            'computer': computer
        }
        # send the template and the computer to the html page
        return render(request, template, context)
    elif request.method == "POST":
        print('computer Id:', computer_id)
        form_data = request.POST
        # check to see if there is a hidden value field with delete and send the id to get deleted
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == 'DELETE'
        ):
            # Connect to the database and delete the computer with the id of the computer from the details page.
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE
                    from
                    hrapp_computer 
                    where id=?

                """, (computer_id,))

            return redirect(reverse('hrapp:computers'))


def confirm_computer_delete(request, computer_id):
    '''
    This function renders the confirm delete html for when the user clicks delete on the details page it passes in the template for 
    that future html and passes the id of the computer they want to delete
    '''
    template = 'computers/computer_delete.html'

    context = {
        'computer_id': int(computer_id)
    }

    return render(request, template, context)


# def create_computer(cursor, row):
#     _row = sqlite3.Row(cursor, row)

#     computer = Computer()
#     computer["id"] = _row["id"]
#     computer["first_name"] = _row["first_name"]
#     computer["last_name"] = _row["last_name"]
#     computer["purchase_date"] = _row["purchase_date"]
#     computer ["unassign_date"] = _row["unassign_date"]
#     computer["make"] = _row["make"]
#     computer["manufacturer"] = _row["manufacturer"]
#     computer["count"] = row["count"]


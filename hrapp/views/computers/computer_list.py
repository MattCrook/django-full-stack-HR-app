import sqlite3
import datetime
from django.shortcuts import render ,redirect
from django.urls import reverse
from hrapp.models import Computer, model_factory, EmployeeComputer
from ..connection import Connection

def computer_list(request):

    #This is just a function to get all the computers and verifies that it is a fet method
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Computer)
            db_cursor = conn.cursor()
            #fetch the table computers from the DB
            db_cursor.execute("""
               SELECT
                c.id,
                c.make,
                c.manufacturer
                from hrapp_computer c
            """)
            #Place the rows into readabel format and fetch them 
            all_computers = db_cursor.fetchall()
            
        #supply the correct information for the render function 1. the location of the html and 2. the info it needs.
        template = 'computers/computer_list.html'

        context = {
            'computers': all_computers,
            'length': len(all_computers)
        }
        return render(request, template, context)
    #check if it is  post method coming in
    elif request.method == "POST":
        #this form_data grabs the needed info from the computer_form.html page and gets ready to appropriate it to sqlite3
        form_data = request.POST
        #connect to that sweet database
        if(
            "actual_method" in form_data and form_data["actual_method"]=="SEARCH"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                conn.row_factory = model_factory(Computer)
                db_cursor = conn.cursor()
                search_query = f"%{form_data['search_results']}%"
                db_cursor.execute("""
                    SELECT
                    * from hrapp_computer
                    where manufacturer like ?
                    or make like ?
                """, (search_query,search_query))
                computers = db_cursor.fetchall()

                template = 'computers/computer_list.html'

                context = {
                    'computers': computers,
                    'length': len(computers)
                }
            return render(request, template, context)
        else:
            with sqlite3.connect(Connection.db_path) as conn:
                conn.row_factory = model_factory(Computer)
                db_cursor = conn.cursor()
                now = datetime.datetime.now()
                assigned_date = now.strftime("%Y-%m-%d")
                
                

                #get the correct information from the db
                db_cursor.execute("""
                    INSERT into hrapp_computer (manufacturer, make, purchase_date)
                    values ( ?, ? , ?)
                """, (
                    #fetch the information by name or by id
                    form_data['manufacturer'], form_data['make'], form_data['purchase_date']
                ))
                computer_id = db_cursor.lastrowid
                if form_data["employee"] != "Not Assigned":
                    unassign_past_computers(form_data["employee"], db_cursor)
                    
                    db_cursor.execute("""
                        INSERT into hrapp_employeecomputer (computer_id, employee_id, assign_date, unassign_date)
                        values(?,?,?, null)

                    """, (
                        (computer_id), form_data['employee'], assigned_date
                    ))

                #send the user back to the master list with the updated computer
                return redirect(reverse('hrapp:computers'))



def get_last_computer():

    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT *
            from hrapp_computer c
        """)

        data= db_cursor.fetchall()[-1]

        return data
    
def unassign_past_computers(id, db_cursor):
    print("ID in test", id)
    now = datetime.datetime.now()
    unassigned_date = now.strftime("%Y-%m-%d")
        

    db_cursor.execute("""
        SELECT id from hrapp_employeecomputer
        where employee_id = ? and unassign_date is null;
    """, (id,))

    data = db_cursor.fetchone()
    if data != None:
        ecId = data.id
        print("date:", unassigned_date, "id:", ecId)
        db_cursor.execute("""
            UPDATE hrapp_employeecomputer
            set unassign_date = ?
            where id = ?;
        """, (unassigned_date, ecId))


        # for row in data:
        #     if row.unassign_date == None:
        #         print(unassigned_date, row.id)
        #         db_cursor.execute("""
        #         UPDATE hrapp_employeecomputer
        #         set unassign_date = ?
        #         where id = ?
        #         """,(unassigned_date, row.id))




    
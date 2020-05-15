import sqlite3
import datetime
from django.shortcuts import render, redirect, reverse
from hrapp.models import TrainingProgram, TrainingProgramEmployee, Employee
from ..connection import Connection
from django.contrib.auth.decorators import login_required
from hrapp.models import model_factory




def training_programs_list(request):
    if request.method == 'GET':
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
                """)
            data = db_cursor.fetchall()
            
            future_tp = []
            past_tp = []
            
            current_date = datetime.date.today()

            for tp_Object in data:
                if datetime.datetime.strptime(tp_Object.start_date,
                '%Y-%m-%d').date() <= current_date:
                    past_tp.append(tp_Object)
                else:
                    future_tp.append(tp_Object)    

        template_name = 'training_programs/training_program_list.html'
        context = {
            'all_training_programs': future_tp,
            'past_training_programs': past_tp
        }
        return render(request, template_name, context)

    elif request.method == 'POST':
        form_data = request.POST
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()
            db_cursor.execute("""
            INSERT INTO hrapp_trainingprogram
            (title, start_date, end_date, capacity
            )
            VALUES (?, ?, ?, ?)
            """,
                (form_data['title'], form_data['start_date'],
                    form_data['end_date'], form_data['capacity']))
        return redirect(reverse('hrapp:trainingprograms'))

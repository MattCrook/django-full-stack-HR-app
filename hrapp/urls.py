from django.urls import path
from django.conf.urls import include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', login_user, name='login'),
    path('admin/', admin_user, name='admin'),
    path('logout/', logout_user, name='logout'),

    path('employees/', employee_list, name='employee_list'),
    path('trainingprograms/', training_programs_list, name='trainingprograms'),
    path('pasttraining/',training_programs_list, name='pasttraining'),
    path('trainingprograms/form/', training_program_form, name='training_program_form'),
    path('trainingprograms/<int:training_program_id>/form', training_program_edit_form, name='training_program_edit_form'),
    path('trainingprograms/<int:training_program_id>/details', training_program_details, name='training_program'),
    path('trainingprograms/<int:training_program_id>/details/attendees', employee_attendees, name='attendees'),
    path('employee/<int:employee_id>', employee_details, name='employee'),
    path('employee/<int:employee_id>/form', employee_edit, name='employee_edit'),
    path('employee/<int:employee_id>/programform', employee_add_program, name='employee_program_form'),
    path('employee/form', employee_add, name='employee_form'),
    path('computers/', computer_list, name="computers"),
    path('computer/<int:computer_id>/', computer_details, name="computer"),
    path('departments/', department_list, name="departments"),
    path('department/<int:department_id>/', department_detail, name="department"),
    path('department/form/', department_form, name="department_form"),
    path('computer/<int:computer_id>/', computer_details, name="computer"),
    path('computer/form/', computer_form, name='computer_form'),
    path('computer/delete/<int:computer_id>/', confirm_computer_delete, name='confirm_computer_delete'),
]

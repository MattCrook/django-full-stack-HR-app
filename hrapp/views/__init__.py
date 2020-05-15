from .home import home
from .auth.logout import logout_user
from .auth.login import login_user, admin_user
from .connection import Connection 
from .departments import department_list, department_detail, department_form
from .computers import computer_list, computer_details, computer_form
from .training_programs.training_programs_list import training_programs_list
from .training_programs.training_program_details import training_program_details
from .training_programs.training_program_form import training_program_form
from .training_programs.training_program_form import training_program_edit_form
from .training_programs.training_programs_attendees import employee_attendees
from .computers import computer_list
from .computers import computer_list, computer_details
from .computers import computer_list, computer_details, computer_form, confirm_computer_delete
from .employees import employee_list, employee_details, employee_edit, employee_add, employee_add_program

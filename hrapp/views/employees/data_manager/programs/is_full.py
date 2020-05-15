from .get_program import get_program
from .current_capacity import current_capacity

def is_full(program_id):
    program_capacity = get_program(program_id).capacity
    current = current_capacity(program_id)
    return program_capacity > current
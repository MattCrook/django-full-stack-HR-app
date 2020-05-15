from django.db import models
from django.urls import reverse
from .employee import Employee
from .training_program import TrainingProgram

class TrainingProgramEmployee(models.Model):
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training_program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "training program employee"
        verbose_name_plural = "training programs employees"
    
    def get_absolute_url(self):
        return reverse("TrainingProgramEmployee_detail", kwargs={"pk": self.pk})
    
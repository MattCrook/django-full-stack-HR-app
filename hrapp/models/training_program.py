from django.db import models
from django.urls import reverse



class TrainingProgram(models.Model):

    title = models.CharField(max_length=55)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()
    employees = models.ManyToManyField(
        "Employee", through='TrainingProgramEmployee', )

    class Meta:
        verbose_name = "trainingprogram"
        verbose_name_plural = "trainingprograms"

    def get_absolute_url(self):
        return reverse("trainingprogram_details", kwargs={"pk": self.pk})

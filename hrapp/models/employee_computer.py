from django.db import models
from django.urls import reverse


class EmployeeComputer(models.Model):
    """
    Creates the join table for the many to many relationship between computers and employees
    Author: Joe Shep
    methods: none
    """

    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    computer = models.ForeignKey("Computer", on_delete=models.CASCADE)
    assign_date = models.DateField()
    unassign_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "computer and employee"
        verbose_name_plural = "computers and employees"

    def get_absolute_url(self):
        return reverse("EmployeeComputer_detail", kwargs={"pk": self.pk})

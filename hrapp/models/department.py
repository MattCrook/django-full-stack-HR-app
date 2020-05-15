from django.urls import reverse
from django.db import models


class Department(models.Model):

    department_name = models.CharField(max_length=25)
    budget = models.FloatField()

    class Meta:
        verbose_name = "department"
        verbose_name_plural = "departments"

    def __str__(self):
        return self.department_name

    def get_absolute_url(self):
        return reverse("Department_detail", kwargs={"pk": self.pk})

from django.db import models


class School(models.Model):
    name = models.CharField(max_length=20)
    max_student = models.IntegerField()

    class Meta:
        ordering = ["id"]


class Student(models.Model):
    student_id = models.CharField(max_length=36)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-first_name"]


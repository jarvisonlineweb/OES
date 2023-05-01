from django.db import models
from .students import Students
from .course import Course


class Carts(models.Model):
    cart_id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.PROTECT)
    course_id=models.ForeignKey(Course,on_delete=models.PROTECT)
    date=models.DateField()
    amount=models.IntegerField(max_length=50)

    class Meta:
        db_table="carts"
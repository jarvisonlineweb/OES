from django.db import models
from .students import Students
from .course import Course



class Course_booking(models.Model):
    course_booking_id=models.AutoField(primary_key=True)
    booking_date=models.DateField(null=True)
    student_id=models.ForeignKey(Students,on_delete=models.PROTECT)
    course_id=models.ForeignKey(Course,on_delete=models.PROTECT)
    booking_status=models.IntegerField(10)
    booking_description=models.CharField(max_length=250,null=False)
    amount=models.IntegerField(null=True)
    payment_status=models.IntegerField(10)
    charges=models.IntegerField(50)
    total_amount=models.IntegerField(50)


    class Meta:
        db_table=" Course_booking"

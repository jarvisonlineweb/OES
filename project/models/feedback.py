from django.db import models
from .students import Students
from .expert import Expert
from .course import Course

class Feedback(models.Model):
    feedback_id=models.AutoField(primary_key=True)
    feedback_description=models.CharField(max_length=250,null=False)
    feedback_date=models.DateField(null=False)
    rate=models.IntegerField(5)
    student_id=models.ForeignKey(Students,verbose_name="Students",default=1,on_delete=models.SET_DEFAULT)
    expert_id=models.ForeignKey(Expert,verbose_name="Expert",default=1,on_delete=models.SET_DEFAULT,null=True)
    course_id=models.ForeignKey(Course,on_delete=models.PROTECT)


    class Meta:
        db_table="Feedback"


from django.db import models
from .students import Students
from .expert import Expert
from .course import Course


class Query(models.Model):
    query_id=models.AutoField(primary_key=True)
    query_description=models.CharField(max_length=250,null=False)
    student_id=models.ForeignKey(Students,verbose_name="Students",default=1,on_delete=models.SET_DEFAULT)
    expert_id=models.ForeignKey(Expert,verbose_name="Expert",default=1,on_delete=models.SET_DEFAULT)
    query_response=models.CharField(max_length=250,null=True)
    course_id=models.ForeignKey(Course,verbose_name="Course",default=1,on_delete=models.SET_DEFAULT)
    query_date=models.DateField(null=False)
    solve_date=models.DateField(null=True)

    class Meta:
        db_table="Query"

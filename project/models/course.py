from django.db import models
from .subjects import Subjects
from .expert import Expert


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50,null=False)
    course_image = models.CharField(null=True,max_length=100)
    course_description = models.CharField(max_length=250,null=False)
    course_duration = models.CharField(max_length=10,null=False)
    course_fees = models.IntegerField(50,null=False)
    course_content = models.CharField(max_length=150,null=False)
    course_timing = models.TimeField(max_length=10,null=True)
    course_level = models.CharField(max_length=50)
    course_language = models.CharField(max_length=50)
    subject_id = models.ForeignKey(Subjects, default=1, on_delete=models.SET_DEFAULT)
    expert_id = models.ForeignKey(Expert,verbose_name="Expert",default=1, on_delete=models.SET_DEFAULT)

    class Meta:
        db_table = "Course"

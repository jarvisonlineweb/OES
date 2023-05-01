from django.db import models
from .course import Course


class Subject_Material(models.Model):
    material_id=models.AutoField(primary_key=True)
    course_id=models.ForeignKey(Course,verbose_name="Course",default=1,on_delete=models.SET_DEFAULT)
    topic=models.CharField(max_length=50,null=False)
    uploaded_date=models.DateField(null=True)
    description=models.CharField(max_length=250)

    class Meta:
        db_table="Subject_Material"

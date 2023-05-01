from django.db import models
from .stream import Stream


class Subjects(models.Model):
    subject_id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=50,null=False)
    description=models.CharField(max_length=250)
    stream_id=models.ForeignKey(Stream,default=1,on_delete=models.SET_DEFAULT)

    class Meta:
        db_table="Subjects"
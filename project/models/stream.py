from django.db import models

class Stream(models.Model):
    stream_id = models.AutoField(primary_key=True)
    stream_type = models.CharField(max_length=50,null=False)
    description = models.CharField(max_length=250)


    class Meta:
        db_table = "Stream"

from django.db import models


class Students(models.Model):
    student_id=models.AutoField(primary_key=True)
    student_name=models.CharField(max_length=50,null=False)
    student_password=models.CharField(max_length=50,null=False)
    student_email = models.EmailField(max_length=150, null=False)
    student_contact=models.CharField(max_length=13,null=False)
    registered_date=models.DateField(null=False)
    is_admin=models.IntegerField(null=True)
    otp = models.CharField(max_length=10, null=True)
    otp_used = models.IntegerField(10,null=True)

    class Meta:
        db_table="Students"

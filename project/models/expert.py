from django.db import models


class Expert(models.Model):
    expert_id=models.AutoField(primary_key=True)
    expert_name=models.CharField(max_length=50,null=False)
    expert_email=models.EmailField(max_length=150,null=False)
    expert_contact=models.CharField(max_length=13,null=False)
    expert_image=models.CharField(null=True,max_length=100)
    expert_password=models.CharField(max_length=100,null=False)
    expert_qualification=models.CharField(max_length=15,null=False)
    expert_experience=models.CharField(max_length=15,null=False)
    registered_date=models.DateField(null=True)
    otp = models.CharField(max_length=10, null=True)
    otp_used = models.IntegerField(10, null=True)

    class Meta:
        db_table="Expert"


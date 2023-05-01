from django import forms
from project.models import Stream, Subjects, Course, Subject_Material, Query, Feedback, Expert, \
    Course_booking, Students
from parsley.decorators import parsleyfy

@parsleyfy
class StrForm (forms.ModelForm):
    class Meta:
        model = Stream
        fields = ["stream_type","description"]


@parsleyfy
class SubForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = ["subject_name","description","stream_id"]


@parsleyfy
class StuForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ["student_id","student_name","student_password","student_email","student_contact"]



@parsleyfy
class CourseForm(forms.ModelForm):
    course_image = forms.FileField()
    class Meta:
        model = Course
        fields = ["course_name", "course_image", "course_description", "course_duration", "course_fees",
                  "course_content", "course_level", "course_language", "subject_id", "expert_id"]


@parsleyfy
class SubmatForm(forms.ModelForm):
    topic = forms.FileField()
    class Meta:
        model = Subject_Material
        fields = ["course_id","topic","description"]

@parsleyfy
class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ["query_description","student_id","expert_id","course_id","query_date"]

@parsleyfy
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["feedback_description","feedback_date","student_id","expert_id"]

@parsleyfy
class ExpertForm(forms.ModelForm):
    expert_image = forms.FileField()
    class Meta:
        model =Expert
        fields = ["expert_name","expert_email","expert_contact","expert_image","expert_password","expert_qualification","expert_experience","registered_date"]

@parsleyfy
class CourbookForm(forms.ModelForm):
    class Meta:
        model = Course_booking
        fields = ["student_id","course_id","booking_status","booking_description","payment_status"]

@parsleyfy
class SturegForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ["student_name","student_email","student_password","student_contact","registered_date","is_admin"]





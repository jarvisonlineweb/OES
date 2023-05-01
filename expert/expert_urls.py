from django.urls import path,include

from client import client_views
from expert import expert_views

urlpatterns = [

    path('expert_index/',expert_views.expert_index),
    path('expert_expert/',expert_views.expert_expert),
    path('expert_student/',expert_views.expert_student),
    path('expert_stream/',expert_views.expert_stream),
    path('expert_course/',expert_views.expert_course),
    path('expert_subject/',expert_views.expert_subject),


    path('expert_submat/',expert_views.expert_submat),
    path('expert_insert_submat/',expert_views.expert_insert_submat),
    path('expert_edit_submat/<int:id>',expert_views.expert_edit_submat),
    path('expert_update_submat/<int:id>',expert_views.expert_update_submat),
    path('expert_delete_subject_material/<int:id>',expert_views.expert_delete_subject_material),

    path('expert_coubooking/',expert_views.expert_course_booking),
    path('expert_course_report1/',expert_views.expert_report1),
    path('expert_course_report2/',expert_views.expert_report2),




    path('expert_query/',expert_views.expert_query),
    path('exp_response/<int:id>',expert_views.expert_response),
    path('expert_feedback/',expert_views.expert_feedback),
    path('expert_editprofile/',expert_views.expert_edit_profile),
    path('expert_updateprofile/',expert_views.expert_update_profile),
    path('expert_logout/', expert_views.expert_logout),

]

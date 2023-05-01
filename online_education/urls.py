"""online_education URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from project import views

from django.urls import re_path as url

from project.views import HomeView, ProjectChart

urlpatterns = [
    path('admin/',admin.site.urls),
    path('user/',views.view),
    path('', views.index),
    path('stream/',views.stream),
    path('delete_stream/<int:id>',views.delete_stream),
    path('insert_stream/',views.insert_stream),
    path('edit_stream/<int:id>',views.edit_stream),
    path('stream_update/<int:id>',views.update_stream),

    path('expert/', views.expert),

    path('course/', views.course),
    path('delete_course/<int:id>', views.delete_course),
    path('insert_course/', views.insert_course),
    path('edit_course/<int:id>', views.edit_course),
    path('update_course/<int:id>', views.update_course),

    path('subjects/', views.subjects),
    path('delete_subject/<int:id>', views.delete_subject),
    path('insert_subject/', views.insert_subject),
    path('edit_subjects/<int:id>', views.edit_subjects),
    path('update_subjects/<int:id>', views.update_subjects),


    path('students/', views.students),

    path('sub_mat/', views.subject_material),
    path('delete_subject_material/<int:id>', views.delete_subject_material),
    path('insert_submat/', views.insert_submat),
    path('insert_submat/<int:id>', views.insert_submat),
    path('edit_submat/<int:id>', views.edit_submat),
    path('update_submat/<int:id>', views.update_submat),

    path('cou_booking/', views.course_booking),
    path('accept_coubooking/<int:id>', views.accept_coubooking),
    path('reject_coubooking/<int:id>', views.reject_coubooking),
    path('report_coubook/', views.report_coubook),
    path('report2_coubook/', views.coubook_report2),
    path('report3_coubook/', views.coubook_report3),
    path('report4_coubook/', views.coubook_report4),
    path('expert_due_amount/', views.expert_due_amount),
    path('paid/<int:id>', views.exert_amount_paid),

    path('query/', views.query),
    path('feedback/', views.feedback),

    path('login/', views.admin_login),
    path('forgot/', views.forgot_password),
    path('sendmail/', views.send_OTP),
    path('reset_pass/', views.set_password),
    path('logout/', views.logout),
    path('edit_profile/', views.edit_profile),
    path('update_profile/', views.update_profile),
    path('index/', views.index),
    path('header/', views.header),

    url(r'charthome', HomeView.as_view(), name='home'),
    url(r'^api/chart/data/$', ProjectChart.as_view(), name="api-data"),

    path('client/', include('client.client_urls')),
    path('expert/', include('expert.expert_urls')),

]

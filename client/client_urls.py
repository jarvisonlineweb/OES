from django.urls import path,include

from client import client_views


urlpatterns = [

    path('home/',client_views.home),
    path('client_login/',client_views.client_login),
    path('client_logout/',client_views.client_logout),
    path('client_forgotpass/',client_views.client_forgot_password),
    path('client_sendmail/',client_views.send_OTP),
    path('client_reset_pass/',client_views.set_password),
    path('client_registration/',client_views.insert_clientregistration),
    path('client_course/<int:id>',client_views.client_course),
    path('client_course/', client_views.client_course),
    path('instructor_course/<int:id>', client_views.instructor_course),
    path('client_cart/',client_views.client_cart),
    path('show/',client_views.show),
    path('client_contactus/',client_views.client_contactus),
    path('client_contactus/<int:id>',client_views.client_contactus),
    # path('client_postquery/',client_views.client_postquery),
    path('client_singlecourse/<int:id>/',client_views.client_singlecourse),
    path('client_insertfeedback/',client_views.client_insertfeedback),
    path('client_editprofile/',client_views.client_editprofile),
    path('client_updateprofile/',client_views.client_updateprofile),
    path('client_cart/',client_views.client_cart),
    #path('delete_cart/<int:id>/',client_views.delete_client_cart),

    path('insert_cart/<int:id>',client_views.insert_cart),
    path('clear_cart/',client_views.clear_cart),
    path('delete_cart/<int:id>',client_views.destroy_cart),
    path('client_header_menu/',client_views.load_menu),
    path('client_header_menu1/<int:id>',client_views.load_menu1),


    path('client_ins_login/',client_views.client_instructor_login),
    path('client_ins_registration/',client_views.insert_ins_registration),
    path('client_ins_forgotpass/',client_views.instructor_forgot_password),
    path('client_ins_sendmail/',client_views.ins_send_OTP),
    path('client_ins_reset_pass/',client_views.ins_set_password),




    path('client_instructors/',client_views.client_instructors),
    path('client_instructors_details/<int:id>/',client_views.client_instructors_details),
    path('client_addtocart/',client_views.client_addtocart),
    path('search/',client_views.autosuggest,name='search1'),
    path('client_checkout/',client_views.client_checkout),
    path('client_payment/',client_views.client_payment),
    path('client_booking/<int:total>',client_views.select_checkout),
    path('client_viewresponse/',client_views.client_view_response),
    path('client_coubook/',client_views.coubook),
    path('success/<int:id>', client_views.success),
    path('cancel/',client_views.cancel),

    path('execute_payment/',client_views.execute_payment),
    path('after_execute_payment/', client_views.after_execute_payment),

]
import sys
from datetime import date
import hashlib

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.conf import settings
import paypalrestsdk
# Create your views here.
from client.cart import Cart
from project.forms import *
from project.functions import handle_uploaded_file
from project.models import Students, Course, Carts, Query
from django.contrib import messages
import random
from online_education import settings
from django.core.mail import send_mail


def home(request):
    exp = Expert.objects.all().count()
    que=Query.objects.all().count()
    cou = Course.objects.all().count()


    feed = Feedback.objects.all().count()
    cou_book = Course_booking.objects.filter(booking_status=1)
    c= Course.objects.all()
    f=Feedback.objects.all()
    print("______________________",f)


    return render(request,"home_client.html",{"expert":exp,"query":que,"course":cou,"feedback":feed,"course_booking":cou_book,"courses":c,"feedbacks":f})

def client_login(request):
    d = date.today()
    d= d.strftime("%Y-%m-%d")
    if request.method == "POST":
            u = request.POST["client_user"]
            p = request.POST["client_password"]
            print("--------------",u)
            print("---------", p)
            newpassword = hashlib.md5(p.encode('utf')).hexdigest()
            print("************&&&&&&&&&&",newpassword)
            val = Students.objects.filter(student_email=u, student_password=newpassword).count()
            print("--------------------------------------", val)
            if val == 1:

                data = Students.objects.filter(student_email=u, student_password=newpassword)

                for items in data:
                    request.session['client_username'] = items.student_email
                    request.session['client_id'] = items.student_id
                    print("---------------",u)


                    if request.POST.get("remember"):
                        response = redirect("/client/home/")
                        response.set_cookie('client_email', request.POST["client_user"], 3600 * 24 * 365 * 2)
                        response.set_cookie('client_pass', request.POST["client_password"], 3600 * 24 * 365 * 2)
                        return response



                    if 'cart' in request.session:
                        product_ids = request.session['cart'].keys()
                        print("----------", product_ids)
                        for course in product_ids:
                            val = request.session['cart'][course]
                            count = 0
                            list1 = []
                            for item in val:
                                list1.append(val[item])
                                print("++++++++++++++++++++++++++",list1)
                                count = count + 1
                                if count == 4:
                                    cc1 = Carts.objects.filter(course_id_id=list1[0]).count()

                                    if cc1 == 0:
                                        d = date.today()
                                        c = Carts(student_id_id=items.student_id, course_id_id=list1[0],amount=int(list1[2]), date=d)
                                        c.save()


                        cart = Cart(request)
                        cart.clear()

                    return HttpResponseRedirect('/client/home/')

            else:
                messages.error(request,"Invalid username and password")
                return render(request,"client_login.html",{"date":d})
    else:
            if request.COOKIES.get("client_email"):
                return render(request, "client_login.html",{'client_email_cookie1': request.COOKIES['client_email'],'client_password_cookie2': request.COOKIES['client_pass'] ,"date":d })  # cookie1 and cookie2 are keys
            else:
                return render(request, "client_login.html",{"date":d})


def client_logout(request):
    try:
        del request.session['client_id']
        del request.session['email']
    except:
        pass

    return redirect("/client/client_login/")





def client_forgot_password(request):
    return render(request,"client_forgot_password.html")





def send_OTP(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST.get('email')
    print("---------------",e)
    request.session['client_username']=e
    obj = Students.objects.filter(student_email=e).count()

    if obj == 1:
        val = Students.objects.filter(student_email=e).update(otp=otp1 , otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject,message,email_from,recipient_list)
        return render(request,"client_reset.html")
    else:
        messages.error(request,'Password does not match')
        return render(request,"client_login.html")






def set_password(request):
    totp = request.POST.get('client_otp')
    tpassword = request.POST.get('client_npass')
    cpassword = request.POST.get('client_cpass')
    print(totp)
    if tpassword == cpassword :
        e = request.session['client_username']
        val = Students.objects.filter(student_email=e,otp=totp,otp_used=0).count()
        print(val)
        if val == 1:
            newpassword = hashlib.md5(tpassword.encode('utf')).hexdigest()
            val = Students.objects.filter(student_email=e).update(otp_used=1,student_password=newpassword)
            return redirect('/client/client_login/')
        else:
            messages.info(request,'OTP does not match')
            return render(request,"client_reset.html")
    else:
        messages.info(request,'New Password & Confirm Password does not match')
        return render(request,"client_reset.html")

    return render(request,"client_reset.html")


def insert_clientregistration(request):
    d = date.today()
    d = d.strftime("%Y-%m-%d")

    if request.method == "POST":

        form = SturegForm(request.POST)
        print("++++++++++++++++++++",form)
        print("----------",form.errors)
        print(form)
        try:
          if form.is_valid():
                try:
                    print("******************************************",form)
                    newform = form.save(commit=False)
                    newform.student_password = hashlib.md5(newform.student_password.encode('utf')).hexdigest()
                    newform.save()
                    return redirect("/client/client_login/")
                except:
                    print("------", sys.exc_info())
          else:
                pass
        except:
              print("------", sys.exc_info())
    else:
        form = SturegForm()
    print("----- date ------------",d)
    return render(request,"client_login.html",{'form':form,'date':d})



def client_course(request,id=0):
    sql1 = "SELECT course_id_id as feedback_id , FLOOR(AVG(rate)) as AVG FROM feedback GROUP by course_id_id"
    q = Feedback.objects.raw(sql1)
    print("----", q)
    if request.method == "POST":
        name = request.POST.get("course_name")
        cou=Course.objects.filter(course_name=name)
    else:

        if id == 0:
            cou=Course.objects.all()

        else:
            cou1=Course.objects.filter(subject_id_id = id)
            page = request.GET.get('page', 1)

            print("page ----------------", page)
            paginator = Paginator(cou1, 1)

            try:
                cou = paginator.page(page)
            except PageNotAnInteger:
                cou = paginator.page(1)
            except EmptyPage:
                cou = paginator.page(paginator.num_pages)
    return render(request, "client_course.html", {'course':cou,"rate":q})




def instructor_course(request,id=0):
    sql1 = "SELECT course_id_id as feedback_id , FLOOR(AVG(rate)) as AVG FROM feedback GROUP by course_id_id"
    q = Feedback.objects.raw(sql1)
    print("----", q)
    cou1=Course.objects.filter(expert_id_id = id)
    page = request.GET.get('page', 1)
    print("page ----------------", page)
    paginator = Paginator(cou1, 3)
    try:
        cou = paginator.page(page)
    except PageNotAnInteger:
            cou = paginator.page(1)
    except EmptyPage:
            cou = paginator.page(paginator.num_pages)
    return render(request, "instructor_course.html", {'course':cou,"rate":q})



def client_contactus(request,id=0):
    qry=Query.objects.all()
    exp=Expert.objects.all()
    cou=Course.objects.all()
    e_id =0
    if request.method=="POST":
        try:
             d=date.today()
             desc=request.POST["query_description"]
             print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",desc)

             course_id = request.POST["course_id"]
             expert_id = request.POST["expert_id"]
             sid=request.session["client_id"]

             print('dadad',d,desc,course_id,expert_id,sid)
             print(type(sid))
             qry=Query(query_date=d, query_description=desc, course_id_id=course_id, expert_id_id=expert_id, student_id_id=sid)
             qry.save()
             return redirect("/client/client_viewresponse/" )

        except:
             print("**************************",sys.exc_info())
    else:
        d = Course.objects.get(course_id = id)
        e_id = d.expert_id_id
        print("----- e_id--------",e_id)
    return render(request,"client_contactus.html",{'query':qry,'expert':exp,'course':cou,"cid":id,"eid":e_id})




def client_singlecourse(request,id):
    cou = Course.objects.get(course_id=id)
    feed = Feedback.objects.filter(course_id=id)
    sub_mate = Subject_Material.objects.filter(course_id=id)
    str=Stream.objects.all()
    cou1=Course.objects.all()
    exp=Course.objects.filter(course_id=id)
    submat=Subject_Material.objects.all()
    total1=0
    print("!!!!!!!!!!!!!!!!!!!!!!",cou1)
    print('-------------')
    print(feed)
    print('++++____',exp)

    sql1 = "SELECT count(*) as course_booking_id FROM ` course_booking` GROUP by course_id_id HAVING course_id_id = %s"

    total = Course_booking.objects.raw(sql1,[id])

    for data in total:
        total1 = data.course_booking_id

    if request.session.has_key('client_id'):
        sid = request.session['client_id']
        sy = Course_booking.objects.filter(course_id_id=id,student_id_id=sid,booking_status=1).count()
        if sy > 0:
            flag=1
        else:
            flag=0
    else:
        flag=0
			
    return render(request,"client_singlecourse.html",{"course":cou,"feedback":feed,"sub_mat1":sub_mate,"stream":str,"courses":cou1,"expert":exp,"submat":submat,"total":total1,"flag":flag})

def client_insertfeedback(request):
    if request.method=="POST":
        try:
             d=date.today()
             desc=request.POST["feedback_description"]
             print(desc)
             rate=request.POST['rate']
             course_id = request.POST["course_id"]
             sid=request.session["client_id"]

             print("++++++++++++++++++++++++++")
             feed=Feedback(feedback_date=d,feedback_description=desc,course_id_id=course_id,student_id_id=sid,rate=rate)
             feed.save()
             return redirect("/client/client_singlecourse/%s" % course_id)

        except:
             print("**************************",sys.exc_info())

    return render(request,"client_course.html")


def client_editprofile(request):
    id = request.session['client_id']
    print("++++++++++++++++++++++++++++++", id)
    stu = Students.objects.get(student_id=id)
    print("**************************", stu)
    return render(request,"client_editprofile.html",{'students': stu})


def client_updateprofile(request):
    id = request.session['client_id']
    stu = Students.objects.get(student_id=id)
    form = StuForm(request.POST, instance=stu)
    print("------", form.errors)

    if form.is_valid():
        try:
            form.save()
            return redirect("/client/home/")
        except:
            print("------", sys.exc_info())
    else:
        pass

    return render(request, "client_editprofile.html", {'students':stu})

def client_cart(request):
    if 'client_id' in request.session:
        id = request.session['client_id']
        c = Carts.objects.filter(student_id_id=id)
        sum = 0
        for val in c:
            sum = sum + val.amount
        print("--- sum -------", sum)
        return render(request,"client_cart.html", {"item": c, "total": sum})

    else:
        cart=Cart(request)
        total=cart.get_total_price()
        print(total)
        return render(request,"client_cart.html",{"total":total})
    return render(request, "client_cart.html")


def delete_client_cart(request,id):
    cou_book = Course_booking.objects.get(course_booking_id=id)
    cou_book.delete()
    return redirect("/client/client_cart/")


def insert_cart(request, id):
    print("inside cart function")
    if 'client_id' in request.session:

        try:
            u = request.session["client_id"]


            fee = request.POST["course_fees"]
            d = date.today().strftime("%Y-%m-%d")
            print("----- User id --------", u,id)
            val = Carts.objects.filter(student_id_id=u,course_id_id=id).count()
            print("----- Insert cart ------",val)
            if val==0:
                C = Carts(student_id_id=u, course_id_id=id,amount=fee, date=d)
                C.save()
        except:
            print("-------", sys.exc_info())
        return redirect('/client/client_cart')
    else:
        try:

            cart = Cart(request)
            product = Course.objects.get(course_id=id)
            print("+++++++++++++++==",product)
            cart.add(product=product)
            print(cart)


        except:
            print("-------", sys.exc_info())

    return redirect('/client/client_cart')

def destroy_cart(request,id):
    if 'client_id' in request.session:
        product = Carts.objects.get(cart_id=id)
        product.delete()
        return redirect('/client/client_cart')


    else:
        cart=Cart(request)
        product=Course.objects.get(course_id=id)
        cart.remove(product)
        return redirect('/client/client_cart')

def clear_cart(request):
    if 'client_id' in request.session:
        product = Carts.objects.all()
        product.delete()
        return redirect('/client/client_cart')
    else:
        cart=Cart(request)
        cart.clear()
        return redirect('/client/client_cart')






def load_menu(request):
    print("--- load menu -----")
    str=Stream.objects.all()
    subj=Subjects.objects.all()
    return render(request,"test.html",{"stream":str,"s":subj})

def load_menu1(request,id):
    print("--- load menu1 -----")
    subj=Subjects.objects.all()
    print("================================================================",id)
    cou=Course.objects.get(course_id=id)
    print("-- ",Subjects.objects.all().count())
    return render(request,"test.html",{"course":cou})


def client_instructors(request):
    exp=Expert.objects.all()
    return render(request,"client_instructors.html",{"expert":exp})

def client_instructors_details(request,id):
    exp=Expert.objects.get(expert_id=id)
    cou=Course.objects.filter(expert_id_id=id)
    print("0000000000000000000000000000000",cou)
    return render(request,"client_instructors_details.html",{"expert":exp,"course":cou})


def client_addtocart(request):
    return render(request,"client_add_to_cart.html")




def autosuggest(request):
    if 'term' in request.GET:
        qs=Course.objects.filter(course_name__istartswith=request.GET.get('term'))

        names = list()

        for x in qs:
            names.append(x.course_name)
        return JsonResponse(names,safe=False)

    return render(request,"client_header_footer.html")


def client_instructor_login(request):
    if request.method == "POST":
        u = request.POST.get("client_user")
        p = request.POST.get("client_password")
        print("--------------", u)
        print("---------", p)
        newpassword = hashlib.md5(p.encode('utf')).hexdigest()
        print("*************&&&&&&&&&&&", newpassword)
        val = Expert.objects.filter(expert_email=u, expert_password=newpassword).count()
        print("--------------------------------------", val)
        if val == 1:

            data = Expert.objects.filter(expert_email=u, expert_password=newpassword)

            for items in data:
                request.session['expert_username'] = items.expert_email
                request.session['expert_id'] = items.expert_id
                print("---------------", u)

            if request.POST.get("remember"):
                response = redirect("/expert/expert_index/")
                response.set_cookie('expert_email', request.POST["client_user"], 3600 * 24 * 365 * 2)
                response.set_cookie('expert_pass', request.POST["client_password"], 3600 * 24 * 365 * 2)
                return response

            return HttpResponseRedirect('/expert/expert_index/')
        else:
            messages.error(request, "Invalid username and password")
            return render(request, "instructor_login.html")
    else:
        if request.COOKIES.get("expert_email"):
            return render(request, "instructor_login.html", {'expert_email_cookie1': request.COOKIES['expert_email'],
                                                         'expert_password_cookie2': request.COOKIES[
                                                             'expert_pass']})  # cookie1 and cookie2 are keys
        else:
            return render(request, "instructor_login.html")




def instructor_forgot_password(request):
    return render(request,"instructor_forgot.html")





def ins_send_OTP(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST.get('email')
    print("---------------",e)
    request.session['expert_username']=e
    obj = Expert.objects.filter(expert_email=e).count()

    if obj == 1:
        val = Expert.objects.filter(expert_email=e).update(otp=otp1 , otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject,message,email_from,recipient_list)
        return render(request,"client_ins_reset.html")
    else:
        messages.error(request,'Password does not match')
        return render(request,"instructor_login.html")






def ins_set_password(request):
    totp = request.POST.get('client_otp')
    tpassword = request.POST.get('client_npass')
    cpassword = request.POST.get('client_cpass')
    print(totp)
    if tpassword == cpassword :
        e = request.session['expert_username']
        val = Expert.objects.filter(expert_email=e,otp=totp,otp_used=0).count()
        print(val)
        if val == 1:
            newpassword = hashlib.md5(tpassword.encode('utf')).hexdigest()
            val = Expert.objects.filter(expert_email=e).update(otp_used=1,expert_password=newpassword)
            return redirect('/client/client_ins_login/')
        else:
            messages.info(request,'OTP does not match')
            return render(request,"client_ins_reset.html")
    else:
        messages.info(request,'New Password & Confirm Password does not match')
        return render(request,"client_ins_reset.html")

    return render(request,"client_ins_reset.html")


def insert_ins_registration(request):

    if request.method == "POST":

        name = request.POST['expert_name']
        email = request.POST['expert_email']
        contact= request.POST['expert_contact']
        image = request.FILES['expert_image']
        password = request.POST['expert_password']
        qualification=request.POST['expert_qualification']
        experience=request.POST['expert_experience']
        expert_password = hashlib.md5(password.encode('utf')).hexdigest()
        red_date = date.today()

        try:
            handle_uploaded_file(request.FILES['expert_image'])

            e = Expert(expert_name=name,expert_email=email,expert_contact=contact,expert_image=image,
                       expert_password=expert_password,expert_qualification=qualification,
                       expert_experience=experience,registered_date=red_date)
            e.save()
            return redirect("/client/client_ins_login/")
        except:
                print("------", sys.exc_info())

    else:

        return render(request,"instructor_login.html")
    return render(request, "instructor_login.html")

import math

def select_checkout(request,total):
    if request.method=="POST":
        if request.session.has_key('client_id'):
            amt = total
            print(amt)
            uid = request.session['client_id']
            date1 = date.today().strftime("%Y-%m-%d")
            c = Carts.objects.filter(student_id_id=uid)
            for data in c:
                cid=data.course_id_id
                amount = data.amount
                charges = math.ceil(amount * 0.10)
                total_amount = amount - charges
                o = Course_booking(student_id_id=uid, amount=int(amount), booking_date=date1, booking_status=0, payment_status=0,course_id_id=cid,charges=charges,total_amount=total_amount)
                o.save()
            id = Course_booking.objects.latest('course_booking_id')
            print("--------------------order id--", id)

    return redirect("/client/client_payment")



def client_checkout(request):

    if "client_id" in request.session:
        u=request.session['client_id']
        student=Students.objects.get(student_id=u)
        cou=Carts.objects.filter(student_id_id=u)
        sum = 0
        for val in cou:
            sum = sum + val.amount
        print("----------", sum)
        return render(request,"client_checkout.html",{"user":student,"course":cou,"total":sum})
    else:
        return redirect("/client/client_login/")


def client_payment(request):
    u = request.session['client_id']
    student = Students.objects.get(student_id=u)
    cou = Carts.objects.filter(student_id_id=u)
    sum = 0
    for val in cou:
        sum = sum + val.amount
    print("----------", sum)
    return render(request,"client_payment.html",{"user":student,"course":cou,"total":sum})






def client_postquery(request):
    if request.method=="POST":
        try:
             d=date.today()
             desc=request.POST["query_description"]
             print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",desc)

             course_id = request.POST["course_id"]
             expert_id = request.POST["expert_id"]
             sid=request.session["client_id"]

             print('ggggsgsgsg',d,desc,course_id,expert_id,sid)

             qry=Query(query_date=d, query_description=desc, course_id_id=course_id, expert_id_id=expert_id, student_id_id=sid)
             qry.save()
             print('sssssssssssssssssssss')
             return redirect("/client/client_contactus/ss" )

        except:
             print("**************************aaaaa",sys.exc_info())

    return render(request,"client_contactus.html")










def client_view_response(request):
    s=request.session['client_id']
    que=Query.objects.filter(student_id_id=s)
    print("000000000000000000000000000",que)
    return render(request,"viewresponse.html",{'query':que})


def show(request):
    if request.method == "POST":
        name = request.POST.get("course_name")
        cou = Course.objects.filter(course_name=name)

    return render(request, "client_course.html", {'course':cou})



def coubook(request):
    id=request.session['client_id']
    coubooking=Course_booking.objects.filter(student_id=id)

    return render(request,"client_coursebooking.html",{'course_booking':coubooking})



def success(request,id):
    cou=Course_booking.objects.get(course_booking_id = id)
    cou.payment_status = 2
    cou.save()
    return redirect('/client/client_coubook/')

def cancel(request):
    return render(request,"cancel.html")




def execute_payment(request):
    id = request.session['client_id']
    coubooking = Course_booking.objects.filter(student_id=id)
    C_id = request.POST["C_id"]
    print(C_id)
    query_string = '?C_id=' + str(C_id)

    paypalrestsdk.configure({
        "mode": "sandbox",  # Change to "live" in production
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/client/after_execute_payment/"+ query_string,
            "cancel_url": "http://127.0.0.1:8000/client/cancel"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": 'test',
                    "sku": "Item001",
                    "price": '1',
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": '1',
                "currency": "USD"
            },
            "description": "School Fees"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        return render(request, "client_coursebooking.html",{'course_booking':coubooking})


def after_execute_payment(request):
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")
    C_id = request.GET.get('C_id')
    cou = Course_booking.objects.get(course_booking_id=int(C_id))
    cou.payment_status = 2
    cou.save()
    # print(cou)
    return render(request, "payment_done.html")
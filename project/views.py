import sys
from django.utils.dateparse import parse_date
import hashlib
from django.shortcuts import render, redirect

from online_education import settings

from project.forms import StrForm, SubForm, SubmatForm, QueryForm, FeedbackForm, ExpertForm, \
    CourbookForm, StuForm, CourseForm

from project.functions import handle_uploaded_file
from project.models import Students,Course_booking,Subject_Material,Feedback,Query,Subjects,Course,Expert,Stream
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.db import connection
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


# Create your views here.




def view(request):
    s=Students.objects.all()
    print("++++++++++++++",Students.objects.all().count())
    return render(request,"Students.html",{'Students':s})

def stream(request):
    str = Stream.objects.all()

    if header(request):
        return render(request,"Stream.html",{"stream":str})
    else:
        return redirect('login/')

def delete_stream(request, id):
    str = Stream.objects.get(stream_id=id)
    str.delete()
    return redirect("/stream/")

def insert_stream(request):
    s = Stream.objects.all()
    if request.method == "POST":
        form = StrForm(request.POST)
        print("----------",form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect("/stream")
            except:
                print("------", sys.exc_info())

        else:
            pass

    else:
        form =StrForm ()

       # return render(request, "Stream.html", {"form": form})

    return render(request,"insert_stream.html",{'form':form,'stream':s})


def edit_stream(request,id):
    str=Stream.objects.get(stream_id=id)
    return render(request,"edit_stream.html",{"stream":str})

def update_stream(request,id):
    str=Stream.objects.get(stream_id=id)
    form=StrForm(request.POST,instance=str)
    print("------",form.errors)

    if form.is_valid():
        try:
            form.save()
            return redirect("/stream")
        except:
            print("------",sys.exc_info())

    return render(request,"edit_stream.html",{"stream":str})


def subjects(request):
    sub=Subjects.objects.all()
    if header(request):
        return render(request,"Subject.html",{"subjects":sub})
    else:
        return redirect('login/')


def delete_subject(request,id):
    sub = Subjects.objects.get(subject_id=id)
    sub.delete()
    return redirect("/subjects/")

def insert_subject(request):
    s=Stream.objects.all()
    sta=Subjects.objects.all()
    if request.method == "POST":
        form = SubForm(request.POST)
        print("++++++++++++++++++++",form)
        print("----------",form.errors)
        if form.is_valid():
            try:
                print("******************************************",form)
                form.save()
                return redirect("/subjects/")
            except:
                print("------", sys.exc_info())

        else:
            pass

    else:
        form =SubForm ()
    return render(request,"insert_subject.html",{'form':form,'stream':s,'subjects':sta})


def edit_subjects(request,id):
    s = Stream.objects.all()
    sub=Subjects.objects.get( subject_id=id)
    return render(request,"edit_subjects.html",{"subjects":sub,'stream':s})

def update_subjects(request,id):
    s = Stream.objects.all()

    sub=Subjects.objects.get(subject_id=id)
    form=SubForm(request.POST,instance=sub)
    print("------",form.errors)

    if form.is_valid():
        try:
            form.save()
            return redirect("/subjects")
        except:
            print("------",sys.exc_info())
    else:
        return render(request,"edit_subjects.html",{"subjects":sub,'stream':s})

    return render(request,"edit_subjects.html",{"subjects":sub,'stream':s})


def students(request):
    stu=Students.objects.all()
    if header(request):
        return render(request,"Students.html",{"students":stu})
    else:
        return redirect('login/')



def expert(request):
    exp=Expert.objects.all()
    if header(request):
        return render(request,"Expert.html",{"expert":exp})
    else:
        return redirect('/login/')



def expert_due_amount(request):

    sql1 = "SELECT c.expert_id_id as id , (select expert_name from expert where expert_id = c.expert_id_id) as course_booking_id ,  sum(charges) as total FROM ` course_booking` b  join course c join expert e where b.course_id_id = c.course_id and c.expert_id_id = e.expert_id GROUP by c.expert_id_id"

    data = Course_booking.objects.raw(sql1)

    return render(request,"expert_charges.html",{"data":data})


def exert_amount_paid(request,id):
    data = Course_booking.objects.select_related('course_id').filter(course_id__expert_id=id)

    for val in data:
        val.charges = 0
        val.save()

    return  redirect('/expert_due_amount/')

def course(request):
    e=Expert.objects.all()
    cou=Course.objects.all()
    print(cou)
    if header(request):
        return render(request, "Course.html",{"course":cou,"expert":e})
    else:
        return redirect('login/')




def delete_course(request,id):
    cou = Course.objects.get(course_id=id)
    cou.delete()
    return redirect("/course/")

def insert_course(request):
    e = Expert.objects.all()
    s = Course.objects.all()
    sub = Subjects.objects.all()
    print('data came')
    if request.method == "POST":
        print('data came')
        form = CourseForm(request.POST,request.FILES)
        print("----------",form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['course_image'])
                form.save()
                return redirect("/course")
            except:
                print("------", sys.exc_info())

        else:
            pass

    else:
        form =CourseForm ()

       # return render(request, "Stream.html", {"form": form})

    return render(request,"insert_course.html",{'form':form,'expert':e,'course':s,'subjects':sub})










def edit_course(request,id):
    e = Expert.objects.all()
    cou=Course.objects.get(course_id=id)
    sub = Subjects.objects.all()
    return render(request,"edit_course.html",{'expert':e,"course":cou,"subjects":sub})



def update_course(request,id):
    e = Expert.objects.all()
    cou=Course.objects.get(course_id=id)
    sub = Subjects.objects.all()
    form=CourseForm(request.POST,instance=cou)
    print("------",form.errors)

    if form.is_valid():
        try:
            form.save()
            return redirect("/course")
        except:
            print("------",sys.exc_info())
    else:
        return render(request,"edit_course.html",{'expert': e,"course":cou,"subjects":sub})

    return render(request,"edit_course.html",{'expert':e,"course":cou,"subjects":sub})













def subject_material(request):
    sub_mat=Subject_Material.objects.all()
    if header(request):
        return render(request, "Subject_Material.html",{"subject_material":sub_mat})
    else:
        return redirect('login/')


def delete_subject_material(request,id):
    sub_mat = Subject_Material.objects.get(material_id=id)
    sub_mat.delete()
    return redirect("/sub_mat/")

def insert_submat(request,id=0):
    c=Course.objects.all()
    sta=Subject_Material.objects.all()
    if request.method == "POST":
        form =SubmatForm(request.POST,request.FILES)
        print("----------",form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['topic'])
                form.save()
                return redirect("/sub_mat")
            except:
                print("------", sys.exc_info())

        else:
            pass

    else:
        form =SubmatForm()

       # return render(request, "Stream.html", {"form": form})

    return render(request,"insert_submat.html",{'form':form,'course':c,'subject_material':sta,'id':id})


def edit_submat(request,id):
    c = Course.objects.all()
    submat = Subject_Material.objects.get(material_id=id)
    return render(request,"edit_submat.html",{"subject_material":submat,'course':c})


def update_submat(request,id):
    c = Course.objects.all()
    submat=Subject_Material.objects.get(material_id=id)
    form=SubmatForm(request.POST,instance=submat)
    print("------",form.errors)

    if form.is_valid():
        try:
            form.save()
            return redirect("/sub_mat")
        except:
            print("------",sys.exc_info())
    else:
        return render(request,"edit_submat.html",{"subject_material":submat,'course':c})

    return render(request,"edit_submat.html",{"subject_material":submat,'course':c})










def course_booking(request):
    cou_book=Course_booking.objects.all()
    if header(request):
        return render(request,"Course_Booking1.html",{"course_booking":cou_book})
    else:
        return redirect('login/')







def accept_coubooking(request,id):
    cou = Course_booking.objects.get(course_booking_id=id)
    cou.booking_status=1
    print(cou)
    cou.save()
    return redirect("/index/")


def reject_coubooking(request,id):
    cou = Course_booking.objects.get(course_booking_id=id)
    cou.booking_status=2
    print(cou)
    cou.save()
    return redirect("/index/")




def query(request):
    que=Query.objects.all()
    if header(request):
        return render(request, "Query.html",{"query":que})
    else:
        return redirect('login/')












def feedback(request):
    feed=Feedback.objects.all()
    print('hiiiii-----------------------###############')
    print(feed)
    if header(request):
        return render(request,"Feedback.html",{"feedback":feed})
    else:
        return redirect('login/')










def admin_login(request):

    if request.method =="POST":
        u = request.POST["email"]
        p = request.POST["password"]
        print("--------------",u)
        print("---------",p)
        newpassword = hashlib.md5(p.encode('utf')).hexdigest()
        val = Students.objects.filter(student_email=u,student_password=newpassword).count()
        print("--------------------------------------",val)
        if val == 1:

            data = Students.objects.filter(student_email=u, student_password=newpassword)

            for items in data:
                request.session['username'] = items.student_email
                request.session['id'] = items.student_id


            if request.POST.get("remember"):
                response = redirect("/index/")
                response.set_cookie('admin_email', request.POST["email"],3600 * 24 * 365 * 2)
                response.set_cookie('admin_pass', request.POST["password"],3600 * 24 * 365 * 2)
                return response

            return HttpResponseRedirect('/index/')

        else:
            messages.error( request, "Invalid username and password" )
            return render(request, "login.html")
    else:
        print("++++++++++++++++++++++++++++")
        print("++++", request.COOKIES.get("admin_email"))
        if request.COOKIES.get("admin_email"):
            print("++++",request.COOKIES.get("admin_email"))
            return render(request, "login.html",
                          {'admin_email_cookie1': request.COOKIES['admin_email'],
                           'admin_password_cookie2': request.COOKIES['admin_pass']})  # cookie1 and cookie2 are keys
        else:
            return render(request, "login.html")





def forgot_password(request):
    return render(request,"forgot_password.html")





def send_OTP(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']
    print("---------------",e)
    request.session['username']=e
    obj = Students.objects.filter(student_email=e).count()

    if obj == 1:
        val = Students.objects.filter(student_email=e,is_admin=1).update(otp=otp1 , otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject,message,email_from,recipient_list)
        return render(request, 'reset.html')
    else:
        messages.error(request,'Password does not match')
        return render(request,"login.html")






def set_password(request):
    totp = request.POST.get('otp')
    tpassword = request.POST.get('npass')
    cpassword = request.POST.get('cpass')
    print(totp)
    password = hashlib.md5(tpassword.encode('utf')).hexdigest()
    if tpassword == cpassword :
        e = request.session['username']
        val = Students.objects.filter(student_email=e,is_admin=1,otp=totp,otp_used=0).count()

        if val == 1:
            val = Students.objects.filter(student_email=e).update(otp_used=1,student_password=password)
            return redirect('/login/')
        else:
            messages.info(request,'OTP does not match')
            return render(request,"reset.html")
    else:
        messages.info(request,'New Password & Confirm Password does not match')
        return render(request,"reset.html")

    return render(request,"reset.html")








def logout(request):
    try:
        del request.session['username']
        del request.session['temail']
    except:
        pass

    return redirect("/login")




def edit_profile(request):
     id = request.session['id']
     print("++++++++++++++++++++++++++++++",id)
     stu = Students.objects.get(student_id=id,is_admin=1)
     print("**************************",stu)
     return render(request,"edit_profile.html",{'students':stu})

def update_profile(request):
     id = request.session['id']
     stu=Students.objects.get(student_id=id)
     form = StuForm(request.POST, instance=stu)
     print("------",form.errors)

     if form.is_valid():
         try:
             form.save()
             return redirect("/index")
         except:
             print("------",sys.exc_info())
     else:
         pass

     return render(request,"edit_profile.html",{'students':stu})








def index(request):
    exp=Expert.objects.all().count()
    cou=Course.objects.all().count()
    feed=Feedback.objects.all().count()
    que=Query.objects.all().count()
    cou_book = Course_booking.objects.filter(booking_status=0)

    if header(request):
        return render(request,"index.html",{"expert":exp,"course":cou,"feedback":feed,"query":que,"co":cou_book})
    else:
        return redirect('/login/')







class HomeView(View):
    def get(self,request, *args,**kwargs):
        return  render(request,"index.html")

class ProjectChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        cursor=connection.cursor()
        cursor.execute('''SELECT (select course_name from course WHERE course_id = b.course_id_id) as name, count(*) FROM ` course_booking` b JOIN course c where b.course_id_id = c.course_id and b.booking_status = 1
GROUP by b.course_id_id''')
        qs=cursor.fetchall()
        print("+++++++++++=")
        labels=[]
        default_items=[]
        for item in qs:
            labels.append(item[0])
            default_items.append(item[1])

        data = {
            "labels":labels,
            "default":default_items,
        }
        return Response(data)

def header(request):
    if request.session.has_key('username'):
        return True
    else:
        return False

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def report_coubook(request):

    exp = Expert.objects.all()

    if request.method == "POST":
        e = request.POST.get("expert")
        print("--- KEyword --------", e)
        cou_book = Course_booking.objects.select_related("course_id").filter(course_id__expert_id_id=e)
        print("---- count --------", Course_booking.objects.select_related("course_id").filter(course_id__expert_id=e))
        return render(request, "report1_data.html", {'course_booking': cou_book, 'expert': exp})
    else:
        cou_book=Course_booking.objects.all()

    return render(request,"Course_Booking_report.html",{'course_booking':cou_book,'expert':exp})



@csrf_exempt
def coubook_report2(request):
    cou = Course.objects.all()
    if request.method == "POST":
        cou = request.POST.get("course")
        print("--- KEyword --------", cou)
        cou_book = Course_booking.objects.filter(course_id_id=int(cou))
        print("---- count --------", Course_booking.objects.filter(course_id_id=int(cou)).count())
        return render(request, "report2_data.html", {'course_booking': cou_book, 'course': cou})
    else:
        cou_book=Course_booking.objects.all()
        return render(request,"Course_Booking_report2.html",{'course_booking':cou_book,'course':cou})




@csrf_exempt
def coubook_report3(request):

    if request.method == "POST":
        start= request.POST["sd"]
        end = request.POST["ed"]

        start = parse_date(start)
        end = parse_date(end)

        if start < end :
            print("----", start, "---------", end)
            cou_book = Course_booking.objects.filter(booking_date__range=[start, end])
            return render(request,"Course_Booking_report3.html",{'course_booking':cou_book})
        else:
            cou_book = Course_booking.objects.all()
            messages.error(request,"start date must be smaller than end date")
            return render(request, "Course_Booking_report3.html", {'course_booking': cou_book})

    else:
        cou_book = Course_booking.objects.all()

    return render(request,"Course_Booking_report3.html",{'course_booking':cou_book})


def coubook_report4(request):

    sql1="SELECT (select student_name from students where student_id = o.student_id_id) as name, sum(amount) as course_booking_id FROM ` course_booking` o  join students u WHERE o.student_id_id = u.student_id group by o.student_id_id"

    cou_book=Course_booking.objects.raw(sql1)
    return render(request,"Course_Booking_report4.html",{'course_booking':cou_book})
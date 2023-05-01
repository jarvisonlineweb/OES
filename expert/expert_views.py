import sys
from datetime import date
import hashlib

from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

from project.forms import SubmatForm, CourbookForm, ExpertForm
from project.models import Students, Course, Feedback, Course_booking, Stream, Expert, Subjects, \
    Subject_Material, Query


def expert_index(request):
    id = request.session['expert_id']
    stu=Course_booking.objects.select_related('course_id').filter(course_id__expert_id=id).count()
    exp=Expert.objects.all().count()
    cou=Course.objects.filter(expert_id_id=id).count()
    feed=Feedback.objects.all().count()
    que=Query.objects.all().count()

    cou_book = Course_booking.objects.select_related('course_id').filter(course_id__expert_id=id, booking_status=0 )

    data = Course_booking.objects.select_related('course_id').filter(course_id__expert_id=id, booking_status=1)

    sum = 0
    for val in data:
        sum = sum + val.charges

    if expert_header(request):
        return render(request,"expert_index.html",{"students":stu,"expert":exp,"course":cou,"feedback":feed,"query":que,"co":cou_book,"sum":sum})
    else:
        return redirect('/client/client_ins_login/')

def expert_expert(request):
    exp=Expert.objects.all()
    if expert_header(request):
        return render(request, "expert_expert.html",{'expert':exp})
    else:
        return redirect('/client/client_ins_login/')


def expert_student(request):
    stu=Students.objects.all()
    if expert_header(request):
        return render(request,"expert_students.html",{'students':stu})
    else:
        return redirect('/client/client_ins_login/')



def expert_stream(request):
    str=Stream.objects.all()
    if expert_header(request):
        return render(request,"expert_stream.html",{'stream':str})
    else:
        return redirect('/client/client_ins_login/')





def expert_course(request):
    id = request.session.get('expert_id')
    cou=Course.objects.filter(expert_id_id=id)
    if expert_header(request):
        return render(request,"expert_course.html",{'course':cou})
    else:
        return redirect('/client/client_ins_login/')



def expert_subject(request):
    sub=Subjects.objects.all()
    if expert_header(request):
        return render(request,"expert_subject.html",{'subjects':sub})
    else:
        return redirect('/client/client_ins_login/')


def expert_submat(request):
    if expert_header(request):
        #submat=Subject_Material.objects.all()
        print("--------- " ,request.session.get('expert_id'))
        id =request.session.get('expert_id')
        submat=Subject_Material.objects.select_related('course_id').filter(course_id__expert_id = id)
        return render(request,"expert_subject_material.html",{'subject_material':submat})
    else:
        return redirect('/client/client_ins_login/')


def expert_insert_submat(request):
    c=Course.objects.all()
    sta=Subject_Material.objects.all()
    if request.method == "POST":
        form =SubmatForm(request.POST)
        print("----------",form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect("/expert/expert_submat")
            except:
                print("------", sys.exc_info())

        else:
            pass

    else:
        form =SubmatForm()

       # return render(request, "Stream.html", {"form": form})

    return render(request,"expert_insert_submat.html",{'form':form,'course':c,'subject_material':sta})


def expert_edit_submat(request,id):
    c = Course.objects.all()
    submat = Subject_Material.objects.get(material_id=id)
    return render(request,"expert_edit_submat.html",{"subject_material":submat,'course':c})


def expert_update_submat(request,id):
    c = Course.objects.all()
    submat=Subject_Material.objects.get(material_id=id)
    form=SubmatForm(request.POST,instance=submat)
    print("------",form.errors)

    if form.is_valid():
        try:
            form.save()
            return redirect("/expert/expert_submat")
        except:
            print("------",sys.exc_info())
    else:
        return render(request,"expert_edit_submat.html",{"subject_material":submat,'course':c})

    return render(request,"expert_edit_submat.html",{"subject_material":submat,'course':c})


def expert_delete_subject_material(request,id):
    sub_mat = Subject_Material.objects.get(material_id=id)
    sub_mat.delete()
    return redirect("/expert/expert_submat/")


def expert_course_booking(request):
    if expert_header(request):
        #coubook=Course_booking.objects.all()
        print("--------- ", request.session.get('expert_id'))
        id = request.session.get('expert_id')
        coubook = Course_booking.objects.select_related('course_id').filter(course_id__expert_id=id)
        return render(request,"expert_course_booking.html",{'course_booking':coubook})
    else:
        return redirect('/client/client_ins_login/')





def expert_query(request):
    if expert_header(request):
        # qry=Query.objects.all()
        print("--------- ", request.session.get('expert_id'))
        id = request.session.get('expert_id')
        que= Query.objects.select_related('course_id').filter(course_id__expert_id=id)
        return render(request, "expert_query.html", {'query': que})
    else:
        return redirect('/client/client_ins_login/')



def expert_response(request,id):
    qry=Query.objects.get(query_id=id)
    if request.method=="POST":
        ex=request.session["expert_id"]
        res=request.POST["query_response"]
        q=Query.objects.get(query_id=id)
        q.query_response=res
        q.save()
        return redirect("/expert/expert_query")


    return render(request,"expert_give_response.html",{"que":qry})

def expert_feedback(request):
    feed=Feedback.objects.all()
    if expert_header(request):
        return render(request,"expert_feedback.html",{'feedback':feed})
    else:
        return redirect('/client/client_ins_login/')





def expert_edit_profile(request):
        id = request.session.get('expert_id')
        print("++++++++++++++++++++++++++++++", id)
        exp = Expert.objects.get(expert_id=id)
        print("**************************", exp)
        return render(request, "expert_edit_profile.html", {'expert': exp})


def expert_update_profile(request):
    id = request.session.get('expert_id')

    name = request.POST['expert_name']
    email = request.POST['expert_email']
    contact = request.POST['expert_contact']
    password = request.POST['expert_password']
    qualification = request.POST['expert_qualification']
    experience = request.POST['expert_experience']
    expert_password = hashlib.md5(password.encode('utf')).hexdigest()
    red_date = date.today()

    try:
        exp = Expert.objects.get(expert_id=id)
        exp.expert_name = name
        exp.expert_email=email
        exp.expert_contact=contact
        exp.expert_password=password
        exp.expert_qualification=qualification
        exp.expert_experience=experience
        exp.registered_date=red_date
        exp.password=expert_password
        exp.save()

        return redirect("/expert/expert_index")
    except:
            print("------", sys.exc_info())

    return render(request, "expert_edit_profile.html", {'expert':exp})




def expert_logout(request):
    del  request.session['expert_id']
    del request.session['expert_username']


    return redirect("/client/client_ins_login/")

def expert_header(request):
    if request.session.has_key('expert_username'):
        return True
    else:
        return False


@csrf_exempt
def expert_report1(request):
    id = request.session.get('expert_id')
    cou=Course.objects.filter(expert_id_id=id)
    if request.method == "POST":
        key = request.POST.get("course_name")
        print("--- KEyword --------", key)

        coubook = Course_booking.objects.filter(course_id__expert_id=id,course_id_id=key)
        return render(request, "expert_report1.html", {'course_booking': coubook,"course":cou})

    else:

        coubook = Course_booking.objects.select_related('course_id').filter(course_id__expert_id=id)
        return render(request,"expert_course_booking_report1.html",{'course_booking':coubook,"course":cou})

@csrf_exempt
def expert_report2(request):
    id = request.session.get('expert_id')
    if request.method == "POST":
        start = request.POST["sd"]
        end = request.POST["ed"]

        start = parse_date(start)
        end = parse_date(end)

        if start < end:
            print("----", start, "---------", end)
            cou_book = Course_booking.objects.filter(booking_date__range=[start, end],course_id__expert_id=id)
            return render(request, "expert_course_booking_report2.html", {'course_booking': cou_book})
        else:
            coubook = Course_booking.objects.select_related('course_id').filter(course_id__expert_id=id)
            messages.error(request, "start date must be smaller than end date")
            return render(request,"expert_course_booking_report2.html",{'course_booking':coubook})

    else:
        id = request.session.get('expert_id')
        coubook = Course_booking.objects.select_related('course_id').filter(course_id__expert_id=id)
        return render(request,"expert_course_booking_report2.html",{'course_booking':coubook})



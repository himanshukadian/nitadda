import json

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404, JsonResponse, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
import os


@csrf_exempt
def checkuserifscrutinyuser(user):
    if user.groups.filter(name="owner").exists() and user.is_superuser:
        return True
    else:
        return False


@csrf_exempt
@login_required(login_url='/owner/login')
@user_passes_test(checkuserifscrutinyuser, login_url="/owner/login/")
def course_list(request):
    course = Course.objects.all()
    return render(request, 'course_list.djt', {'course': coursee})


@csrf_exempt
@login_required(login_url="/")
@user_passes_test(checkuserifscrutinyuser, login_url="/owner/login/")
def Add_Course(request):
    response = {}
    if request.method == 'POST':
        course = Course()
        course.title = request.POST['title']
        course.save()
        return redirect('/owner/add_course')

    return render(request, 'add_course.djt', response)


@csrf_exempt
@login_required(login_url="/")
@user_passes_test(checkuserifscrutinyuser, login_url="/owner/login/")
def Add_Subject(request):
    response = {}
    courses = Course.objects.all()
    response["courses"] = courses
    if request.method == 'POST':
        subject = Subject()
        subject.title = request.POST['title']
        subject.course = Course.objects.get(id=request.POST['courses'])
        subject.save()
        return redirect('/owner/add_subject')

    return render(request, 'add_subject.djt', response)


@csrf_exempt
@login_required(login_url="/")
@user_passes_test(checkuserifscrutinyuser, login_url="/owner/login/")
def index(request):
    response = {}
    return render(request, 'base.djt', response)


@csrf_exempt
def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/owner/login/')


@csrf_exempt
def admin_login(request):
    response = {}
    if request.user.is_authenticated:
        logout(request)
    else:
        response = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.groups.filter(name="owner").exists() and user.is_superuser:
                        return HttpResponseRedirect('/owner/')
                    else:
                        # logout(request)
                        return HttpResponseRedirect('/')
                else:
                    response['message'] = 'User is not active yet'
            else:
                response['message'] = 'User is invalid'

        return render(request, 'signin.djt', response)


def Display_Note(request, noteid):
    response = {}
    cd = Note.objects.get(note_id=noteid)
    path = os.path.join(settings.BASE_DIR)
    print(path)
    response["data"] = str(path) + "/media/" + str(cd.notes_pdf)
    return render(request, 'show_notes.djt', response)


@csrf_exempt
@login_required(login_url="/")
def Delete_Note(request, noteid):
    response = {}
    cd = Note.objects.get(note_id=noteid)
    cd.delete()
    return redirect('/owner/all_note')


@csrf_exempt
@login_required(login_url="/")
def UploadNote(request):
    response = {}
    courses = Course.objects.all()
    response["courses"] = courses
    subjects=Subject.objects.all()
    # subjects = []
    # coursesubjects = Subject.objects.values('course', 'course_id')
    # courses = {item['course'] for item in coursesubjects}
    # for course in courses:
    #     subject = Subject.objects.filter(course=course)
    #     subjects.append(subject)
    response["subjects"] = subjects
    if request.method == 'POST':
        cnt = Note_Count.objects.get()
        year = datetime.datetime.now().year
        yy = str(year)
        p1 = yy[2:]
        p2 = str(cnt.note_cnt).zfill(4)
        cnt.note_cnt = cnt.note_cnt + 1
        cnt.save()
        Name = "NOTE"
        noteID = Name + p1 + p2
        print(noteID)
        note = Note()
        # course=Course()
        note.note_id = noteID
        note.title = request.POST['title']
        # course.title=request.POST['courses']
        note.subject = Subject.objects.get(id=request.POST['subjects'])
        note.course = Course.objects.get(id=request.POST['courses'])
        note.notes_pdf = request.FILES["files"]
        note.save()
        return redirect('/owner/upload_note')

    return render(request, 'Upload_Notes.djt', response)


@csrf_exempt
@login_required(login_url="/")
def Get_Note(request):
    response = {}
    notes = Note.objects.all()
    n = len(notes)
    allnotes = []
    coursenotes = Note.objects.values('course', 'course_id')
    courses = {item['course'] for item in coursenotes}
    for course in courses:
        note = Note.objects.filter(course=course)
        allnotes.append(note)
    response["allnotes"] = allnotes
    return render(request, 'all_Notes.djt', response)


@csrf_exempt
@login_required(login_url="/")
def Get_Course(request):
    response = {}
    courses = Course.objects.all()
    response["courses"] = courses
    return render(request, 'all_Courses.djt', response)


@csrf_exempt
@login_required(login_url="/")
def Get_Subject(request):
    response = {}
    subjects = Subject.objects.all()
    response["subjects"] = subjects
    return render(request, 'all_Subjects.djt', response)



@csrf_exempt
@login_required(login_url="/")
def Show_Note(request,courseid):
    response = {}
    notes = Note.objects.all()
    allnotes = []
    note = Note.objects.filter(course=courseid)
    allnotes.append(note)
    response["allnotes"] = allnotes
    return render(request, 'all_Notes.djt', response)


@csrf_exempt
@login_required(login_url="/")
def Get_Subject_Note(request):
    response = {}
    notes = Note.objects.all()
    n = len(notes)
    allnotes = []
    subjectnotes = Note.objects.values('subject', 'subject_id')
    subjects = {item['subject'] for item in subjectnotes}
    for subject in subjects:
        note = Note.objects.filter(subject=subject)
        allnotes.append(note)
    response["allnotes"] = allnotes
    return render(request, 'all_Subject_Notes.djt', response)


@csrf_exempt
@login_required(login_url="/")
def Show_Subject_Note(request,subjectid):
    response = {}
    notes = Note.objects.all()
    allnotes = []
    note = Note.objects.filter(subject=subjectid)
    allnotes.append(note)
    response["allnotes"] = allnotes
    return render(request, 'all_Subject_Notes.djt', response)


@csrf_exempt
def getSubjects(request):
    if request.method == 'POST':
        course_name = request.POST.get('cn')
        print("ajax course_name ", course_name," yo")
        result_set = []
        answer = str(course_name).strip()
        try:
            selected_course = Course.objects.get(title=answer)
        except Course.DoesNotExist:
            selected_course = Course.objects.all()[0]
        print("selected course name ", selected_course)
        all_cities = selected_course.subject_set.all()
        for subject in all_cities:
            print("Subject name ", subject.title)
            result_set.append({'title': subject.title, 'id': subject.id})
            # print("this",json.dumps(result_set));
        return HttpResponse(json.dumps(result_set), content_type='application/json')
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
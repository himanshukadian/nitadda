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
@user_passes_test(checkuserifscrutinyuser, login_url="/owner/login/")
def UploadNote(request):
    response = {}
    courses = Course.objects.all()
    response["courses"] = courses
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
        print(note[0].title)
        allnotes.append(note)
    response["allnotes"] = allnotes
    return render(request, 'all_Notes.djt', response)

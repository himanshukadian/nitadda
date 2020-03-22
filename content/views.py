import json
from django.conf import settings
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
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
    return render(request, 'course_list.djt', {'course': course})


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

    return render(request, 'add_course.html', response)


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

    return render(request, 'add_subject.html', response)


@csrf_exempt
@login_required(login_url="/")
@user_passes_test(checkuserifscrutinyuser, login_url="/owner/login/")
def index(request):
    response = {}
    print(request.user)
    note = Note.objects.all()
    # note = Note.objects.filter(course=courseid).annotate(num_votes=Count('upvotes')).order_by('-num_votes')

    lstatus = []
    providers = []
    for n in note:
        prv = CustomUser.objects.get(id=n.user_id)
        providers.append(prv.username)
        if n.upvotes.filter(id=request.user.id).exists():
            lstatus.append(True)
        else:
            lstatus.append(False)
    response['data'] = zip(note, lstatus, providers)
    return render(request, 'all_Notes.html', response)

    # response = {}
    # print("index was called!!")
    # print(request.user)
    # notes = Note.objects.all()
    # lstatus = []
    # providers = []
    # for n in notes:
    #     prv = CustomUser.objects.get(id=n.user_id)
    #     providers.append(prv.username)
    #     if n.upvotes.filter(id=request.user.id).exists():
    #         lstatus.append(True)
    #     else:
    #         lstatus.append(False)
    # response['data'] = zip(notes, lstatus, providers)
    # return render(request, 'home.html', response)


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

        return render(request, 'signin.html', response)


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
    subjects = Subject.objects.all()
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
        note.note_pdf = request.FILES["files"]
        note.user_id = request.user.id;
        note.save()
        return redirect('/owner/upload_note')

    return render(request, 'Upload_Notes.html', response)


# @csrf_exempt
# @login_required(login_url="/")
# def Get_Note(request):
#     response = {}
#     notes = Note.objects.all()
#     n = len(notes)
#     allnotes = []
#     coursenotes = Note.objects.values('course', 'course_id')
#     courses = {item['course'] for item in coursenotes}
#     for course in courses:
#         note = Note.objects.filter(course=course)
#         allnotes.append(note)
#     response["allnotes"] = allnotes
#     return render(request, 'all_Notes.html', response)


@csrf_exempt
@login_required(login_url="/")
def Get_Course(request):
    response = {}
    courses = Course.objects.all()
    response["courses"] = courses
    return render(request, 'all_Courses.html', response)


@csrf_exempt
@login_required(login_url="/")
def Get_Subject(request):
    response = {}
    subjects = Subject.objects.all()
    response["subjects"] = subjects
    return render(request, 'all_Subjects.html', response)


@csrf_exempt
@login_required(login_url="/")
def Show_Note(request, courseid):
    response = {}
    print(request.user)
    notes = Note.objects.all()
    note = Note.objects.filter(course=courseid).annotate(num_votes=Count('upvotes')).order_by('-num_votes')

    lstatus=[]
    providers = []
    for n in note:
        prv = CustomUser.objects.get(id=n.user_id)
        providers.append(prv.username)
        if n.upvotes.filter(id=request.user.id).exists():
            lstatus.append(True)
        else:
            lstatus.append(False)
    response['data'] = zip(note, lstatus, providers)
    return render(request, 'all_Notes.html', response)


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
    return render(request, 'all_Subject_Notes.html', response)


@csrf_exempt
@login_required(login_url="/")
def Show_Subject_Note(request, subjectid):
    response = {}
    notes = Note.objects.all()
    allnotes = []
    note = Note.objects.filter(subject=subjectid)
    allnotes.append(note)
    response["allnotes"] = allnotes
    return render(request, 'all_Subject_Notes.html', response)


@csrf_exempt
def getSubjects(request):
    if request.method == 'POST':
        course_name = request.POST.get('cn')
        result_set = []
        answer = str(course_name).strip()
        try:
            selected_course = Course.objects.get(title=answer)
        except Course.DoesNotExist:
            selected_course = Course.objects.all()[0]
        all_cities = selected_course.subject_set.all()
        for subject in all_cities:
            result_set.append({'title': subject.title, 'id': subject.id})
        return HttpResponse(json.dumps(result_set), content_type='application/json')
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )



def Display_Pdf(request,noteid) :
    response = {}
    cd = Note.objects.get(note_id=noteid)
    response["data"] = cd
    return render(request, 'show_note_pdf.html', response)


@login_required(login_url="/")
def Upvote(request):
    print("yaa Upvote called")
    if request.method == 'POST':
        user = request.user
        noteid = request.POST.get('noteid')
        answer = str(noteid).strip()
        print(noteid)
        note = Note.objects.get(note_id=answer)
        if note.upvotes.filter(id=user.id).exists():
            note.upvotes.remove(user)
            alreadyVoted = True
        else:
            note.upvotes.add(user)
            alreadyVoted = False
    data=[]
    data.append(alreadyVoted)
    data.append(noteid)
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@login_required(login_url="/")
def Approve_Note(request, noteid):
    print("approved id : ", noteid)
    cd = Note.objects.get(note_id=noteid)
    course = Course.objects.get(title=cd.course)
    print("course id :", course.id)
    cd.is_approved = True
    url = "/owner/shownote/" + str(course.id)
    print("url " + url)
    cd.save()
    return redirect(url)


@login_required(login_url="/")
def Show_Liked_Notes(request):
    all_notes = Note.objects.all()
    liked_notes = []
    lstatus = []
    providers = []
    response = {}
    for note in all_notes:
        if note.upvotes.filter(id=request.user.id).exists():
            liked_notes.append(note)
            prv = CustomUser.objects.get(id=note.user_id)
            providers.append(prv.username)
            lstatus.append(True)

    response['data'] = zip(liked_notes, lstatus, providers)
    if len(liked_notes) > 0:
        response['user_has_liked'] = True;
    else:
        response['user_has_liked'] = False;
    return render(request, 'liked_notes.html', response)


@login_required(login_url="/")
def Show_Uploaded_Notes(request):
    uploaded_notes = Note.objects.filter(user_id=request.user.id)
    print("got length: ", len(uploaded_notes))
    print("name :", uploaded_notes[0].title)
    response = {}

    response['data'] = uploaded_notes
    if len(uploaded_notes) > 0:
        response['user_has_uploaded'] = True;
    else:
        response['user_has_uploaded'] = False;
    return render(request, 'uploaded_notes.html', response)

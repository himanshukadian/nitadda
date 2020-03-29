import json
from django.conf import settings
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404, JsonResponse, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib import messages
from content.decorators import login_required_message
from django.contrib.auth.decorators import login_required


@csrf_exempt
def checkuserifscrutinyuser(user):
    if user.groups.filter(name="owner").exists() and user.is_superuser:
        return True
    else:
        return False


@csrf_exempt
@login_required(login_url='/content/login')
@user_passes_test(checkuserifscrutinyuser, login_url="/content/login/")
def course_list(request):
    course = Course.objects.all()
    return render(request, 'course_list.djt', {'course': course})


@csrf_exempt
@login_required(login_url="/content/login")
@user_passes_test(checkuserifscrutinyuser, login_url="/content/login/")
def Add_Course(request):
    response = {}
    if request.method == 'POST':
        course = Course()
        course.title = request.POST['title']
        course.duration = request.POST['duration']
        course.no_of_semesters = request.POST['no_of_sem']
        course.save()
        return redirect('/content/add_course')

    return render(request, 'content/add_course.html', response)


@csrf_exempt
@login_required(login_url="/content/login")
@user_passes_test(checkuserifscrutinyuser, login_url="/content/login/")
def Add_Subject(request):
    response = {}
    courses = Course.objects.all()
    response["courses"] = courses
    if request.method == 'POST':
        subject = Subject()
        subject.title = request.POST['title']
        subject.course = Course.objects.get(id=request.POST['courses'])
        subject.save()
        return redirect('/content/add_subject')

    return render(request, 'content/add_subject.html', response)


@csrf_exempt
@login_required(login_url="/content/login")
@user_passes_test(checkuserifscrutinyuser, login_url="/content/login/")
def index(request):
    response = {}
    print(request.user," home tab clicked : RENDER HOME ")
    note = Note.objects.all()[:3]
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
    messages.add_message(request, 20, 'Home tab')
    info = messages.get_messages(request)
    response = {'message': info}
    return render(request, 'home.html', response)
111
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
    messages.success(request, "you have been logged out.")
    return HttpResponseRedirect('/content/login/')


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
                        return HttpResponseRedirect('/content/')
                    else:
                        messages.success(request, 'You are successfully logged in.')
                        return HttpResponseRedirect('/')
                else:
                    messages.warning(request, 'User is not active yet')
                    response['message'] = 'User is not active yet'
            else:
                messages.warning(request, 'User is invalid')
                response['message'] = 'User is invalid'

        return render(request, 'account/signin.html', response)


def Display_Note(request, noteid):
    response = {}
    cd = Note.objects.get(note_id=noteid)
    path = os.path.join(settings.BASE_DIR)
    print(path)
    response["data"] = str(path) + "/media/" + str(cd.notes_pdf)
    return render(request, 'show_notes.djt', response)


@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Delete_Note(request, noteid):
    response = {}
    cd = Note.objects.get(note_id=noteid)
    cd.delete()
    messages.success(request, 'successfully deleted')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this.")
@login_required
def UploadContent(request):
    response = {}
    courses = Course.objects.all()
    response["courses"] = courses
    subjects = Subject.objects.all()
    response["subjects"] = subjects
    if request.method == 'POST':
        if request.POST['content_type']=="note":
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
            messages.success(request, "Successfully Uploaded Notes")
            return redirect('/content/upload/')

        elif request.POST['content_type'] == "paper":
            cnt = Exam_Paper_Count.objects.get()
            year = datetime.datetime.now().year
            yy = str(year)
            p1 = yy[2:]
            p2 = str(cnt.paper_cnt).zfill(4)
            cnt.paper_cnt = cnt.paper_cnt + 1
            cnt.save()
            paper = Exam_Paper()
            name = "PAPER"
            paperID = name + p1 + p2
            print("ID OF PAPER : ", paperID)
            paper.paper_id = paperID
            print("YE HAI WO SUBJECT ID: ", request.POST.get('subjects2'))
            paper.subject = Subject.objects.get(id=request.POST.get('subjects2'))
            paper.course = Course.objects.get(id=request.POST['courses'])

            paper.batch_year = str(request.POST['batch'])[0:4]
            paper.semester = request.POST['semesters']
            paper.exam = request.POST['exams']
            paper.exam_type = request.POST['types']
            paper.title = str(paper.subject.title) + " : " + str(paper.exam)
            paper.paper_pdf = request.FILES["files"]
            paper.user_id = request.user.id;
            paper.save()
            messages.success(request, "Successfully Uploaded Exam Paper.")
            return redirect('/content/upload/')

    return render(request, 'content/Upload_Notes.html', response)

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Get_Course(request):
    response = {}
    courses = Course.objects.all()
    response["courses"] = courses
    return render(request, 'content/all_Courses.html', response)


@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Get_Subject(request):
    response = {}
    subjects = Subject.objects.all()
    response["subjects"] = subjects
    return render(request, 'content/all_Subjects.html', response)


@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Show_Note(request, slug):
    response = {}
    print(request.user)
    cname = Course.objects.get(slug=slug)
    notes = Note.objects.filter(course=cname.id).annotate(num_votes=Count('upvotes')).order_by('-num_votes')
    papers = Exam_Paper.objects.filter(course=cname.id).order_by('-batch_year')
    print(cname)
    lstatus=[]
    providers = []
    for n in notes:
        prv = CustomUser.objects.get(id=n.user_id)
        providers.append(prv.username)
        if n.upvotes.filter(id=request.user.id).exists():
            lstatus.append(True)
        else:
            lstatus.append(False)
    response['data'] = zip(notes, lstatus, providers)
    year = []
    for p in papers:
        if p.semester%2 != 0:
            p.semester += 1
        x = int(p.batch_year - p.semester/2)
        year.append(x)
    response['papers'] = zip(papers, year)
    # response['year'] = year
    response['cname'] = cname
    return render(request, 'content/all_Notes.html', response)


@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required
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
    return render(request, 'content/all_Subject_Notes.html', response)


@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Show_Subject_Note(request, slug):
    response = {}
    print(request.user)
    notes = Note.objects.all()
    sname = Subject.objects.get(slug=slug)
    note = Note.objects.filter(subject=sname.id).annotate(num_votes=Count('upvotes')).order_by('-num_votes')
    print(sname)
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
    response['sname'] = sname
    return render(request, 'content/all_Subject_Notes.html', response)

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
        all_subjects = selected_course.subject_set.all()
        for subject in all_subjects:
            result_set.append({'title': subject.title, 'id': subject.id})
        return HttpResponse(json.dumps(result_set), content_type='application/json')

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Display_Pdf(request,noteid) :
    response = {}
    cd = Note.objects.get(note_id=noteid)
    response["data"] = cd
    return render(request, 'content/show_note_pdf.html', response)


@login_required(login_url="/content/login")
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
@login_required(login_url="/content/login")
def Approve_Note(request, noteid):
    print("approved id : ", noteid)
    cd = Note.objects.get(note_id=noteid)
    course = Course.objects.get(title=cd.course)
    print("course id :", course.id)
    if cd.is_approved:
        messages.success(request, "already approved")
    else:
        cd.is_approved = True
        messages.success(request, 'Successfully approved')
    url = "/content/course_notes/" + str(course.id)
    print("url " + url)
    cd.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# @csrf_exempt
# @login_required_message(message="You should be logged in, in order to perform this.")
# @login_required
# def UploadPaper(request):
#     response = {}
#     courses = Course.objects.all()
#     response["courses"] = courses
#     subjects = Subject.objects.all()
#     response["subjects"] = subjects
#     if request.method == 'POST':
#         cnt = Exam_Paper_Count.objects.get()
#         year = datetime.datetime.now().year
#         yy = str(year)
#         p1 = yy[2:]
#         p2 = str(cnt.paper_cnt).zfill(4)
#         cnt.paper_cnt = cnt.paper_cnt + 1
#         cnt.save()
#         paper = Exam_Paper()
#         name = "PAPER"
#         paperID = name + p1 + p2
#         print("ID OF PAPER : ",paperID)
#         paper.paper_id = paperID
#         print("YE HAI WO SUBJECT ID: ",request.POST.get('subjects2'))
#         paper.subject = Subject.objects.get(id=request.POST.get('subjects2'))
#         paper.course = Course.objects.get(id=request.POST['courses'])
#
#         paper.batch_year = str(request.POST['batch'])[0:3]
#         paper.semester = request.POST['semesters']
#         paper.exam = request.POST['exams']
#         paper.exam_type = request.POST['types']
#         paper.title = str(paper.subject.title) +" : " + str(paper.exam)
#         paper.paper_pdf = request.FILES["files"]
#         paper.user_id = request.user.id;
#         paper.save()
#         messages.success(request, "Successfully Uploaded Exam Paper.")
#         return redirect('/content/upload_paper/')
#
#     return render(request, 'content/Upload_Notes.html', response)

@csrf_exempt
def getCourseDuration(request):
    if request.method == 'POST':
        course_name = request.POST.get('cn')
        answer = str(course_name).strip()
        try:
            selected_course = Course.objects.get(title=answer)
        except Course.DoesNotExist:
            selected_course = Course.objects.all()[0]
        duration = selected_course.duration
        result_set=duration
        # result_set.append({'duration':duration})
        return HttpResponse(json.dumps(result_set), content_type='application/json')

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Display_Paper_Pdf(request,paperid) :
    response = {}
    cd = Note.objects.get(note_id=paperid)
    response["data"] = cd
    return render(request, 'content/show_note_pdf.html', response)
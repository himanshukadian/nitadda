import json
from django.conf import settings
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404, JsonResponse, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from .models import *
from accounts.models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib import messages
from content.decorators import login_required_message
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.generics import ListAPIView




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
    blogs = Blog.objects.all()[:4]
    print(request.user," home tab clicked : RENDER HOME ")
    for b in blogs:
        if len(b.description) > 300:
            b.description = b.description[:300]

    response['blogs'] = blogs
    return render(request, 'home.html', response)

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
    response["this_note"] = cd
    print(cd.total_upvotes)
    response["data"] = str(path) + "/media/" + str(cd.notes_pdf)
    return render(request, 'show_notes.djt', response)


@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Delete_Note(request, noteid):
    cd = Note.objects.get(note_id=noteid)
    cd.delete()
    messages.success(request, 'successfully deleted')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Delete_Paper(request, paperid):
    cd = Exam_Paper.objects.get(pk=paperid)
    cd.delete()
    messages.success(request, 'Successfully deleted Exam Paper')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Delete_Book(request, bookid):
    cd = Book.objects.get(pk=bookid)
    cd.delete()
    messages.success(request, 'Successfully deleted Book')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this.")
@login_required
def UploadContent(request):
    response = {}
    courses = Course.objects.all()
    response["courses"] = courses
    colleges = College.objects.all()
    response["colleges"] = colleges
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
            note.college = College.objects.get(id=request.POST['colleges'])
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
            paper.college =  College.objects.get(id=request.POST['colleges'])
            paper.batch_year = str(request.POST['batch'])[0:4]
            print(paper.batch_year)
            paper.semester = request.POST['semesters']
            paper.exam = request.POST['exams']
            paper.exam_type = request.POST['types']
            paper.title = str(paper.subject.title) + " (" + paper.exam_type + ")"
            paper.paper_pdf = request.FILES["files"]
            paper.user_id = request.user.id;
            paper.save()
            messages.success(request, "Successfully Uploaded Exam Paper.")
            return redirect('/content/upload/')
        else:
            cnt = Book_Count.objects.get()
            year = datetime.datetime.now().year
            yy = str(year)
            p1 = yy[2:]
            p2 = str(cnt.book_cnt).zfill(4)
            cnt.book_cnt = cnt.book_cnt + 1
            cnt.save()
            Name = "BOOK"
            bookID = Name + p1 + p2
            print(bookID)
            book = Book()
            # course=Course()
            book.book_id = bookID
            book.title = request.POST['title']
            book.author = request.POST['author']
            book.subject = Subject.objects.get(id=request.POST['subjects'])
            book.college = College.objects.get(id=request.POST['colleges'])
            book.course = Course.objects.get(id=request.POST['courses'])
            book.user_id = request.user.id
            book.upload_type = request.POST['book_upload_type']
            if book.upload_type == "L":
                book.flink = request.POST["link"]
            else:
                book.book_pdf = request.FILES["file"]
            book.save()
            messages.success(request, "Successfully Uploaded Book")
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
    if request.method == 'POST' and request.POST.get('colleges') is not "0":
        clg = request.POST.get('colleges')
        print("CLG ID: ", clg)
        print("content type ", request.POST.get('content_type'))
        response['current_tab'] = request.POST.get('content_type')
        notes = Note.objects.filter(course=cname.id, college=clg).annotate(num_votes=Count('upvotes')).order_by('-num_votes')
        print("Length notes= ", len(notes))
        papers = Exam_Paper.objects.filter(course=cname.id, college=clg).order_by('-batch_year')
        print("Length papers= ", len(papers))
        books = Book.objects.filter(course=cname.id, college=clg)
        print("Length books= ", len(books))
    else:
        clg = 0
        print("is  0")
        response['current_tab'] = "note"
        notes = Note.objects.filter(course=cname.id).annotate(num_votes=Count('upvotes')).order_by('-num_votes')
        papers = Exam_Paper.objects.filter(course=cname.id).order_by('-batch_year')
        books = Book.objects.filter(course=cname.id)
    colleges = College.objects.all()
    print(cname)
    lstatus=[]
    for n in notes:
        if len(n.title) > 80:
            n.title = n.title[:80] + '...'
        prv = CustomUser.objects.get(id=n.user_id)
        if n.upvotes.filter(id=request.user.id).exists():
            lstatus.append(True)
        else:
            lstatus.append(False)
    response['data'] = zip(notes, lstatus)

    for p in papers:
        if len(p.title) > 20:
            p.title = p.title[:20] + '...'
    response['papers'] = papers

    for b in books:
        if len(b.title) > 20:
            b.title = b.title[:20] + '...'
    response['books'] = books
    response['cname'] = cname
    if clg:
        response['current_college_id'] = clg
    else:
        response['current_college_id'] = "0"
    response['colleges'] = colleges
    return render(request, 'content/all_Notes.html', response)


# @csrf_exempt
# @login_required_message(message="You should be logged in, in order to perform this")
# @login_required
# def Get_Subject_Note(request):
#     response = {}
#     notes = Note.objects.all()
#     n = len(notes)
#     allnotes = []
#     subjectnotes = Note.objects.values('subject', 'subject_id')
#     subjects = {item['subject'] for item in subjectnotes}
#     for subject in subjects:
#         note = Note.objects.filter(subject=subject)
#         allnotes.append(note)
#     response["allnotes"] = allnotes
#     return render(request, 'content/all_Subject_Notes.html', response)


@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Show_Subject_Note(request, slug):
    response = {}
    print(request.user)
    sname = Subject.objects.get(slug=slug)
    if request.method == 'POST' and request.POST.get('colleges') is not "0":
        clg = request.POST.get('colleges')
        print("CLG ID: ", clg)
        print("content type ", request.POST.get('content_type'))
        response['current_tab'] = request.POST.get('content_type')
        notes = Note.objects.filter(subject=sname.id, college=clg).annotate(num_votes=Count('upvotes')).order_by(
            '-num_votes')
        print("Length notes= ", len(notes))
        papers = Exam_Paper.objects.filter(subject=sname.id, college=clg).order_by('-batch_year')
        print("Length papers= ", len(papers))
        books = Book.objects.filter(subject=sname.id, college=clg)
        print("Length books= ", len(books))
    else:
        clg = 0
        print("is  0")
        response['current_tab'] = "note"
        notes = Note.objects.filter(subject=sname.id).annotate(num_votes=Count('upvotes')).order_by('-num_votes')
        papers = Exam_Paper.objects.filter(subject=sname.id).order_by('-batch_year')
        books = Book.objects.filter(subject=sname.id)
    colleges = College.objects.all()
    print(sname)
    lstatus = []
    for n in notes:
        if len(n.title) > 80:
            n.title = n.title[:80] + '...'
        prv = CustomUser.objects.get(id=n.user_id)
        if n.upvotes.filter(id=request.user.id).exists():
            lstatus.append(True)
        else:
            lstatus.append(False)
    response['data'] = zip(notes, lstatus)

    for p in papers:
        if len(p.title) > 20:
            p.title = p.title[:20] + '...'
    response['papers'] = papers

    for b in books:
        if len(b.title) > 20:
            b.title = b.title[:20] + '...'
    response['books'] = books
    response['sname'] = sname
    if clg:
        response['current_college_id'] = clg
    else:
        response['current_college_id'] = "0"
    response['colleges'] = colleges
    # return render(request, 'content/all_Notes.html', response)
    return render(request, 'content/all_Subject_Notes.html', response)

@csrf_exempt
def getSubjects(request):
    if request.method == 'POST':
        course_name = request.POST.get('cn')
        result_set = []
        trimmed_id = str(course_name).strip()
        try:
            selected_course = Course.objects.get(title=trimmed_id)
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
def Display_Pdf(request, noteid):
    response = {}
    cd = Note.objects.get(note_id=noteid)
    response["this_data"] = cd

    if cd.upvotes.filter(username__contains=request.user.username):
        print("user has liked ")
        user_has_liked = True
    else:
        print("user has not liked ")
        user_has_liked = False
    response['user_has_liked'] = user_has_liked
    response['data_type'] = "note"
    return render(request, 'content/show_note_pdf.html', response)

@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Display_Paper_Pdf(request, paperid):
    response = {}
    cd = Exam_Paper.objects.get(pk=paperid)
    response["this_data"] = cd
    response["data_type"] = "paper"
    return render(request, 'content/show_note_pdf.html', response)

@login_required_message(message="You should be logged in, in order to perform this")
@login_required
def Display_Book_Pdf(request, bookid):
    response = {}
    cd = Book.objects.get(pk=bookid)
    if(cd.upload_type == 'L'):
        return redirect(str(cd.flink))
    else:
        response["this_data"] = cd
        response["data_type"] = "book"
        return render(request, 'content/show_note_pdf.html', response)


@login_required(login_url="/content/login")
def Upvote(request):
    print("yaa Upvote called")
    if request.method == 'POST':
        user = request.user
        noteid = request.POST.get('noteid')
        trimmed_id = str(noteid).strip()
        print(noteid)
        note = Note.objects.get(note_id=trimmed_id)
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

@login_required(login_url="/content/login")
def Upvote_Blog(request):
    print("Blog upvote")
    if request.method == 'POST':
        user = request.user
        blogid = request.POST.get('blogid')
        blog = Blog.objects.get(id=blogid)
        if blog.upvotes.filter(id=user.id).exists():
            blog.upvotes.remove(user)
            alreadyVoted = True
        else:
            blog.upvotes.add(user)
            alreadyVoted = False
    data=[]
    data.append(alreadyVoted)
    data.append(blogid)
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required(login_url="/content/login")
def report_post(request, post_id):
    print("Report post called for", post_id)
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=request.user.id)
        trimmed_id = str(post_id).strip()
        if trimmed_id[0] == 'N':
            data_type = "note"
        elif trimmed_id[0] == 'P':
            data_type = "paper"
        else:
            data_type = "blog"
        if data_type == "note":
            note = Note.objects.get(note_id=trimmed_id)
            if note.reports.filter(id=request.user.id).exists():
                already_reported = True
            else:
                note.reports.add(request.user)
                already_reported = False
                print('Report post message recieved.')
                newMessage = ContactUsMessage()
                newMessage.sender_name = user.first_name
                newMessage.email = user.email
                newMessage.phone = user.mobile
                newMessage.subject =  '<REPORTED Notes having ID ' + trimmed_id + '> ' + request.POST['subject']
                newMessage.message = request.POST['message']
                superuser = CustomUser.objects.filter(is_superuser=True).first()
                superuser.notifications = superuser.notifications + 1
                superuser.noti_messages = superuser.noti_messages + '<li> New message has arrived in inbox </li>'
                superuser.save()
                newMessage.save()
                messages.add_message(request, messages.INFO, 'You have successfully reported these notes.Thank you for feedback')
            response={}
            response['already_reported'] = already_reported
            response['note_id'] = post_id
            return Display_Pdf(request, post_id)
        elif data_type == "paper":
            print("trimmed id", trimmed_id)
            paper = Exam_Paper.objects.get(paper_id=trimmed_id)
            if paper.reports.filter(id=request.user.id).exists():
                already_reported = True
            else:
                paper.reports.add(request.user)
                already_reported = False
                print('Report post message recieved.')
                newMessage = ContactUsMessage()
                newMessage.sender_name = user.first_name
                newMessage.email = user.email
                newMessage.phone = user.mobile
                newMessage.subject =  '<REPORTED Exam paper having ID ' + trimmed_id + '> ' + request.POST['subject']
                newMessage.message = request.POST['message']
                superuser = CustomUser.objects.filter(is_superuser=True).first()
                superuser.notifications = superuser.notifications + 1
                superuser.noti_messages = superuser.noti_messages + '<li> New message has arrived in inbox </li>'
                superuser.save()
                newMessage.save()
                messages.add_message(request, messages.INFO, 'You have successfully reported this exam paper.Thank you for feedback')
            response={}
            response['already_reported'] = already_reported
            response['note_id'] = post_id
            return Display_Pdf(request, post_id)

        else:
            blog = Blog.objects.get(id=trimmed_id)
            if blog.reports.filter(id=request.user.id).exists():
                already_reported = True
            else:
                blog.reports.add(request.user)
                already_reported = False
                print('Report post message recieved.')
                newMessage = ContactUsMessage()
                newMessage.sender_name = user.first_name
                newMessage.email = user.email
                newMessage.phone = user.mobile
                newMessage.subject = '<REPORTED News Blog having ID ' + trimmed_id + '> ' + request.POST['subject']
                newMessage.message = request.POST['message']
                superuser = CustomUser.objects.filter(is_superuser=True).first()
                superuser.notifications = superuser.notifications + 1
                superuser.noti_messages = superuser.noti_messages + '<li> New message has arrived in inbox </li>'
                superuser.save()
                newMessage.save()
                messages.add_message(request, messages.INFO, 'You have successfully reported this news blog.Thank you for feedback')
            response = {}
            response['already_reported'] = already_reported
            response['note_id'] = post_id
            return Show_Full_Blog(request, post_id)

    else:
        print('Report post message ERROR.')
        return render(request, 'all_Notes.html')
    # if request.method == 'POST':
    #
    #     return redirect('accounts:index')
    # else:
    #     print('Contact us message ERROR.')
    #     return render(request, 'home.html')


    # return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@login_required(login_url="/content/login")
@user_passes_test(checkuserifscrutinyuser, login_url="/content/login/")
def Approve_Note(request, noteid):
    cd = get_object_or_404(Note, note_id=noteid)
    course = get_object_or_404(Course, title=cd.course)
    if cd.is_approved:
        messages.success(request, "already approved")
    else:
        cd.is_approved = True
        cd.user.notifications = cd.user.notifications + 1
        cd.user.noti_messages = cd.user.noti_messages + '<li> Admin has approved your note titled ' + str(cd.title)
        messages.success(request, 'Successfully approved')
    cd.save()
    cd.user.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
@login_required(login_url="/content/login")
@user_passes_test(checkuserifscrutinyuser, login_url="/content/login/")
def Approve_Paper(request, paperid):
    cd = get_object_or_404(Exam_Paper, pk=paperid)
    # course = get_object_or_404(Course, title=cd.course)
    if cd.is_approved:
        messages.success(request, "already approved")
    else:
        cd.is_approved = True
        cd.user.notifications = cd.user.notifications + 1
        cd.user.noti_messages = cd.user.noti_messages + '<li> Admin has approved your paper : ' + str(cd.title) + '</li>'
        messages.success(request, 'Successfully approved Exam Paper')
    cd.save()
    cd.user.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
@login_required(login_url="/content/login")
@user_passes_test(checkuserifscrutinyuser, login_url="/content/login/")
def Approve_Book(request,bookid):
    cd = get_object_or_404(Book, pk=bookid)
    # course = get_object_or_404(Course, title=cd.course)
    if cd.is_approved:
        messages.success(request, "already approved")
    else:
        cd.is_approved = True
        cd.user.notifications = cd.user.notifications + 1
        cd.user.noti_messages = cd.user.noti_messages + '<li> Admin has approved your book : ' + str(cd.title) + '</li>'
        messages.success(request, 'Successfully approved Book')
    cd.save()
    cd.user.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
def getCourseDuration(request):
    if request.method == 'POST':
        course_name = request.POST.get('cn')
        trimmed_id = str(course_name).strip()
        try:
            selected_course = Course.objects.get(title=trimmed_id)
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

# class NoteTableData(ListAPIView):
#     serializer_class = NoteSerializers

#     def get_queryset(self, *args, **kwargs):
#         print('ha notes table data')
#         filter_category = self.request.GET.get("filter_category")
#         if filter_category==0:
#             queryset = Note.objects.filter()
#         else:
#             queryset = Note.objects.filter(college=filter_category)
#         queryset_filtered = queryset.filter()
#         return queryset_filtered

@csrf_exempt
@login_required(login_url="/content/login")
def Show_Full_Blog(request, blog_id):
    response = {}
    cd = Blog.objects.get(id=blog_id)
    response["this_blog"] = cd

    if cd.upvotes.filter(username__contains=request.user.username):
        print("user has liked ")
        user_has_liked = True
    else:
        print("user has not liked ")
        user_has_liked = False
    response['user_has_liked'] = user_has_liked
    return render(request, 'content/blog_detail.html', response)

@csrf_exempt
@login_required(login_url="/content/login")
def All_Blogs(request):
    response = {}
    blogs = Blog.objects.all()
    print(request.user, " home tab clicked : RENDER HOME ")
    for b in blogs:
        if len(b.description) > 300:
            b.description = b.description[:300]

    response['blogs'] = blogs
    return render(request, 'content/all_blogs.html', response)
from django.db import models
from django.core.validators import FileExtensionValidator
from django.template.defaultfilters import slugify
from django.utils.text import slugify
from accounts.models import CustomUser

class College(models.Model):
    name = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=30, unique=True, editable=False)
    abbreviation = models.CharField(max_length=10, default='')
    # courses_provided = models.CharField(max_length=10, default='')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            while True:
                try:
                    college = College.objects.get(slug=slug)
                    if college == self:
                        self.slug = slug
                        break
                    else:
                        slug = slug + '_'
                except:
                    self.slug = slug
                    break
        super(College, self).save()

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=30, unique=True, editable=False)
    duration = models.IntegerField(default=4)
    no_of_semesters = models.IntegerField(default=8)
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            while True:
                try:
                    course = Course.objects.get(slug=slug)
                    if course == self:
                        self.slug = slug
                        break
                    else:
                        slug = slug + '_'
                except:
                    self.slug = slug
                    break
        super(Course, self).save()

    def __str__(self):
        return self.title

class Subject(models.Model):
    title = models.CharField(max_length=255, default='')
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=30, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title, self.course)
            while True:
                try:
                    subject = Subject.objects.get(slug=slug)
                    if subject == self:
                        self.slug = slug
                        break
                    else:
                        slug = slug + '_'
                except:
                    self.slug = slug
                    break
        super(Subject, self).save()
    def __str__(self):
        return self.title


def get_note_path(instance, filename):
    return 'Note/{0}/pdf/{1}'.format(instance.note_id, filename)

def get_paper_path(instance, filename):
    return 'Exam_Paper/{0}/pdf/{1}'.format(instance.paper_id, filename)

def get_book_path(instance, filename):
    return 'Book/{0}/pdf/{1}'.format(instance.book_id, filename)

class Note(models.Model):
    note_id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(CustomUser, verbose_name="Provider", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=300, default="")
    college = models.ForeignKey(College, verbose_name="College", on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(Subject, verbose_name="Subject",on_delete=models.CASCADE,blank=True, null=True)
    note_pdf = models.FileField(upload_to=get_note_path,
                                   validators=[FileExtensionValidator(["pdf"])],
                                   null=True, blank=True, default=None)

    reports = models.ManyToManyField(CustomUser, related_name='reports')
    upvotes = models.ManyToManyField(CustomUser, related_name='upvotes')

    @property
    def total_reports(self):
        return self.reports.count()

    @property
    def total_upvotes(self):
        return self.upvotes.count()

    is_approved = models.BooleanField(default=False)
    def __unicode__(self):
        return str(self.note_id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Note, self).save(*args, **kwargs)



class Note_Count(models.Model):
    note_cnt = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.note_cnt)

class Exam_Paper(models.Model):
    paper_id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(CustomUser, verbose_name="Provider", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=300, default="")
    college = models.ForeignKey(College, verbose_name="College", on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(Subject, verbose_name="Subject",on_delete=models.CASCADE,blank=True, null=True)
    batch_year = models.IntegerField()
    semester = models.IntegerField()
    exam = models.CharField(max_length=20)
    EXAM_TYPES = (('T', "Theory"), ('P', "Practical"))
    exam_type = models.CharField(max_length=1, choices=EXAM_TYPES, default='T')

    paper_pdf = models.FileField(upload_to=get_paper_path,
                                 validators=[FileExtensionValidator(["pdf"])],
                                 null=True, blank=True, default=None)

    reports = models.ManyToManyField(CustomUser, related_name='paper_reports')

    @property
    def total_reports(self):
        return self.reports.count()

    # upvotes = models.ManyToManyField(CustomUser, related_name='upvotes')
    # @property
    # def total_upvotes(self):
    #     return self.upvotes.count()

    is_approved = models.BooleanField(default=False)
    def __unicode__(self):
        return str(self.paper_id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Exam_Paper, self).save(*args, **kwargs)

class Exam_Paper_Count(models.Model):
    paper_cnt = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.paper_cnt)

class Book(models.Model):
    UPLOAD_TYPES = (('L', 'Link'), ('P', 'PDF'))
    book_id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=300)
    user = models.ForeignKey(CustomUser, verbose_name="Provider", on_delete=models.CASCADE, blank=True, null=True)
    author = models.CharField(max_length=300)
    college = models.ForeignKey(College, verbose_name="College", on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(Subject, verbose_name="Subject", on_delete=models.CASCADE, blank=True, null=True)
    # image = models.ImageField(default='download.jpg', upload_to='books/')
    flink = models.CharField(max_length=300, blank=True)

    upload_type = models.CharField(max_length=1, choices=UPLOAD_TYPES, default='L')
    slug = models.SlugField(max_length=30, unique=True, editable=False)
    book_pdf = models.FileField(upload_to=get_book_path,
                                 validators=[FileExtensionValidator(["pdf"])],
                                 null=True, blank=True, default=None)

    reports = models.ManyToManyField(CustomUser, related_name='book_reports')
    is_approved = models.BooleanField(default=False)
    @property
    def total_reports(self):
        return self.reports.count()


    def __unicode__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title, self.course)
            while True:
                try:
                    book = Book.objects.get(slug=slug)
                    if book == self:
                        self.slug = slug
                        break
                    else:
                        slug = slug + '_'
                except:
                    self.slug = slug
                    break
        super(Book, self).save()


class Blog(models.Model):

    title = models.CharField(max_length=300)
    description = models.CharField(max_length=10000)
    author = models.ForeignKey(CustomUser, verbose_name="Provider", on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField()
    college = models.ForeignKey(College, verbose_name="College", on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(default='download.jpg', upload_to='blogs/')

    reports = models.ManyToManyField(CustomUser, related_name='blog_reports',  blank=True)
    upvotes = models.ManyToManyField(CustomUser, related_name='blog_upvotes', blank=True)

    @property
    def total_reports(self):
        return self.reports.count()

    @property
    def total_upvotes(self):
        return self.upvotes.count()

    is_approved = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

class Book_Count(models.Model):
    book_cnt = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.book_cnt)
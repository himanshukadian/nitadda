from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.urls import reverse_lazy

from content.models import Course, Subject, Blog


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'yearly'

    def items(self):
        return ['accounts:index', 'content:team','content:Get_Course','content:Get_Subject','content:Upload_Content','accounts:profile','password_reset','accounts:register','content:admin_login','content:admin_logout']

    def location(self, item):
        return reverse(item)


class Course_Notes_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Course.objects.all()

    def location(self, item):
        return reverse_lazy('content:Course_Note', kwargs={'slug': item.slug})


class Subject_Notes_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Subject.objects.all()

    def location(self, item):
        return reverse_lazy('content:Subject_Note', kwargs={'slug': item.slug})


class Blogs_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Blog.objects.all()

    def location(self, item):
        return reverse_lazy('content:blogs', kwargs={'blog_id': item.id})
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader
from models import Blog


def blog_home_view(request):
    all_blog_model = Blog.objects.all()
    template = loader.get_template("blog_home.html")
    context = {
        'blog_model': all_blog_model,
    }
    return HttpResponse(template.render(context, request))


def blog_details_view(request):
    blog_index = request.GET['id']
    blog_model = Blog.objects.get(blog_index=blog_index)
    template = loader.get_template("blog_details.html")
    context = {
        'blog_model': blog_model,
    }
    return HttpResponse(template.render(context, request))

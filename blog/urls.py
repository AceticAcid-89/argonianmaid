from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.blog_home_view, name="blog_home"),
    url(r'^view/', views.blog_details_view, name="bolg_details_view"),
]

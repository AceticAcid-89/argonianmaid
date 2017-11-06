from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.home_page_view, name="home_page"),
]
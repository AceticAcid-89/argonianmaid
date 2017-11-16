from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.steam_image_home, name="steam_home"),
    url(r'^artwork/', views.artwork_view, name="artwork_view"),
    url(r'^screenshots/', views.screenshots_view, name="screenshots_view"),
]

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'file_storage'
urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<email>[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)/$', views.UserDetail.as_view()),
    url(r'^pictures/$', views.PictureList.as_view()),
    url(r'^pictures/upload/$', views.upload_picture),
    url(r'^pictures/(?P<filename>[a-zA-Z0-9_.]+)$', views.download_picture),
]
urlpatterns = format_suffix_patterns(urlpatterns)


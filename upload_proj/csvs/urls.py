from django.urls import path
from .views import upload_file_view, response

app_name='csvs'
urlpatterns=[
    path('',upload_file_view,name='upload-view'),
    path('response',response,name='response')
]
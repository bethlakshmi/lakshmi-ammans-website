from django.conf.urls import url
from shastra_compedium.views import (
    UploadChapter,
)

app_name = "shastra_compedium"

urlpatterns = [
    url(r'^chapter/add/$', UploadChapter.as_view(), name='chapter-add'),
]

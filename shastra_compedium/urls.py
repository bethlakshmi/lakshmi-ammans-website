from django.conf.urls import url
from shastra_compedium.views import (
	CategoryCreate,
	CategoryUpdate,
    UploadChapter,
)

app_name = "shastra_compedium"

urlpatterns = [
    url(r'^chapter/add/$', UploadChapter.as_view(), name='chapter-add'),
    url(r'^category/add/$',
        CategoryCreate.as_view(),
        name='category-add'),
    url(r'^category/update/(?P<pk>.*)/$',
        CategoryUpdate.as_view(),
        name='category-update'),
]

from django.conf.urls import url
from shastra_compedium.views import (
	CategoryCreate,
	CategoryUpdate,
    ShastraCreate,
    ShastraUpdate,
    SourceCreate,
    SourceUpdate,
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
    url(r'^shastra/add/$',
        ShastraCreate.as_view(),
        name='shastra-add'),
    url(r'^shastra/update/(?P<pk>.*)/$',
        ShastraUpdate.as_view(),
        name='shastra-update'),
    url(r'^source/add/$',
        SourceCreate.as_view(),
        name='source-add'),
    url(r'^source/update/(?P<pk>.*)/$',
        SourceUpdate.as_view(),
        name='source-update'),
]

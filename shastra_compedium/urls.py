from django.conf.urls import url
from shastra_compedium.views import (
    CategoryCreate,
    CategoryDetailUpdate,
    CategoryUpdate,
    PositionCreate,
    PositionDetailFormSetView,
    PositionList,
    PositionUpdate,
    ShastraCreate,
    ShastraUpdate,
    SourceCreate,
    SourceList,
    SourceUpdate,
    UploadChapter,
)


app_name = "shastra_compedium"

urlpatterns = [
    url(r'^chapter/add/$', UploadChapter.as_view(), name='chapter-add'),
    url(r'^positiondetail/edit/(?P<source_id>\d+)/(?P<category_id>\d*)/?$',
        PositionDetailFormSetView.as_view(),
        name='position-detail-update'),
    url(r'^positiondetail/edit/(?P<position_id>\d+)/?$',
        PositionDetailFormSetView.as_view(),
        name='position-detail-update'),
    url(r'^category/add/$',
        CategoryCreate.as_view(),
        name='category-add'),
    url(r'^category/update/(?P<pk>.*)/$',
        CategoryUpdate.as_view(),
        name='category-update'),
    url(r'^categorydetail/update/(?P<pk>.*)/$',
        CategoryDetailUpdate.as_view(),
        name='categorydetail-update'),
    url(r'^position/add/(?P<order>\d+)/(?P<category>\d+)/$',
        PositionCreate.as_view(),
        name='position-add'),
    url(r'^position/add/$',
        PositionCreate.as_view(),
        name='position-add'),
    url(r'^position/list/?', PositionList.as_view(), name='position_list'),
    url(r'^position/update/(?P<pk>.*)/$',
        PositionUpdate.as_view(),
        name='position-update'),
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
    url(r'^source/list/?', SourceList.as_view(), name='source_list'),
]

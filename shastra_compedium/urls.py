from django.conf.urls import url
from shastra_compedium.views import (
    BulkImageUpload,
    CategoryCreate,
    CategoryDetailUpdate,
    CategoryUpdate,
    DanceStyleCreate,
    DanceStyleUpdate,
    DanceStyleView,
    ExampleImageCopy,
    ExampleImageCreate,
    ExampleImageUpdate,
    ImageList,
    PerformerCreate,
    PerformerUpdate,
    PerformerView,
    PositionCreate,
    PositionDetailFormSetView,
    PositionList,
    PositionUpdate,
    PositionView,
    ShastraCreate,
    ShastraUpdate,
    ShastraChapterView,
    SourceCreate,
    SourceToImageFormSetView,
    SourceList,
    SourceUpdate,
    UploadChapter,
)


app_name = "shastra_compedium"

urlpatterns = [
    url(r'^chapter/add/$', UploadChapter.as_view(), name='chapter-add'),
    url(r'^chapter/add/(?P<category_id>\d+)/$',
        UploadChapter.as_view(),
        name='chapter-additional'),
    url(r'^posdetail/editimages/(?P<source_id>\d+)/(?P<category_id>\d*)/?$',
        SourceToImageFormSetView.as_view(),
        name='position-detail-image-update'),
    url(r'^positiondetail/edit/(?P<source_id>\d+)/cat/(?P<category_id>\d*)/?$',
        PositionDetailFormSetView.as_view(),
        name='position-detail-update'),
    url(r'^positiondetail/edit/(?P<position_id>\d+)/?$',
        PositionDetailFormSetView.as_view(),
        name='position-detail-update'),
    url(r'^positiondetail/edit/(?P<source_id>\d+)/pos/(?P<position_id>\d*)/?$',
        PositionDetailFormSetView.as_view(),
        name='position-detail-update-refined'),
    url(r'^category/add/$',
        CategoryCreate.as_view(),
        name='category-add'),
    url(r'^category/update/(?P<pk>.*)/$',
        CategoryUpdate.as_view(),
        name='category-update'),
    url(r'^categorydetail/update/(?P<pk>.*)/$',
        CategoryDetailUpdate.as_view(),
        name='categorydetail-update'),
    url(r'^image/update/(?P<pk>.*)/$',
        ExampleImageUpdate.as_view(),
        name='exampleimage-update'),
    url(r'^image/add/(?P<image_id>\d+)$',
        ExampleImageCreate.as_view(),
        name='exampleimage-add'),
    url(r'^image/copy/(?P<example_id>\d+)$',
        ExampleImageCopy.as_view(),
        name='exampleimage-copy'),
    url(r'^position/add/(?P<order>\d+)/(?P<category>\d+)/$',
        PositionCreate.as_view(),
        name='position-add'),
    url(r'^position/add/$',
        PositionCreate.as_view(),
        name='position-add'),
    url(r'^performer/add/$',
        PerformerCreate.as_view(),
        name='performer-add'),
    url(r'^performer/update/(?P<pk>.*)/$',
        PerformerUpdate.as_view(),
        name='performer-update'),
    url(r'^performer/view/(?P<pk>.*)/$',
        PerformerView.as_view(),
        name='performer-view'),
    url(r'^dancestyle/add/$',
        DanceStyleCreate.as_view(),
        name='dancestyle-add'),
    url(r'^dancestyle/update/(?P<pk>.*)/$',
        DanceStyleUpdate.as_view(),
        name='dancestyle-update'),
    url(r'^dancestyle/view/(?P<pk>.*)/$',
        DanceStyleView.as_view(),
        name='dancestyle-view'),
    url(r'^position/list/?', PositionList.as_view(), name='position_list'),
    url(r'^image/list/?', ImageList.as_view(), name='image_list'),
    url(r'^position/update/(?P<pk>.*)/$',
        PositionUpdate.as_view(),
        name='position-update'),
    url(r'^position/view/(?P<pk>.*)/$',
        PositionView.as_view(),
        name='position-view'),
    url(r'^source/chapter/(?P<shastra_pk>.*)/(?P<category_pk>.*)/$',
        ShastraChapterView.as_view(),
        name='shastrachapter-view'),
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
    # Images
    url(r'^image/upload/?',
        BulkImageUpload.as_view(),
        name='image_upload'),
]

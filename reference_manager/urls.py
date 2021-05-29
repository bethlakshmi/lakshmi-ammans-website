from django.conf.urls import url
from reference_manager.views import (
    TagCreate,
    TagUpdate,
    URLSourceCreate,
    URLSourceUpdate,
)


app_name = "reference_manager"

urlpatterns = [
    url(r'^tag/add/(?P<pk>.*)/$',
        TagCreate.as_view(),
        name='tag-add'),
    url(r'^tag/update/(?P<pk>.*)/$',
        TagUpdate.as_view(),
        name='tag-update'),
    url(r'^url/add/$',
        URLSourceCreate.as_view(),
        name='source-add'),
    url(r'^url/update/(?P<pk>.*)/$',
        URLSourceUpdate.as_view(),
        name='source-update'),
]

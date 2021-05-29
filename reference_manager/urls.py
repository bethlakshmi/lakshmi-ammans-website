from django.conf.urls import url
from reference_manager.views import (
    URLSourceCreate,
    URLSourceUpdate,
)


app_name = "reference_manager"

urlpatterns = [
    url(r'^url/add/$',
        URLSourceCreate.as_view(),
        name='category-add'),
    url(r'^url/update/(?P<pk>.*)/$',
        URLSourceUpdate.as_view(),
        name='category-update'),
]

# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from shastra_compedium.views import (
    CategoryAutocomplete,
    CombinationAutocomplete,
    PositionAutocomplete,
    PositionDetailAutocomplete,
    PositionDetailExampleAutocomplete,
)


urlpatterns = [
    # add your own patterns here
    url(
        r'^category-autocomplete/$',
        CategoryAutocomplete.as_view(),
        name='category-autocomplete',
    ),
    url(
        r'^combination-autocomplete/$',
        CombinationAutocomplete.as_view(),
        name='combination-autocomplete',
    ),
    url(
        r'^positiondetail-autocomplete/$',
        PositionDetailAutocomplete.as_view(),
        name='positiondetail-autocomplete',
    ),
    url(
        r'^positiondetail-example-autocomplete/$',
        PositionDetailExampleAutocomplete.as_view(),
        name='positiondetail-example-autocomplete',
    ),
    url(
        r'^position-autocomplete/$',
        PositionAutocomplete.as_view(),
        name='position-autocomplete',
    ),
    url(r'^', include('shastra_compedium.urls')),
] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)

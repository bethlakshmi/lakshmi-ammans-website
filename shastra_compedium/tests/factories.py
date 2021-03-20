from django.contrib.auth.models import User
from factory import (
    Sequence,
    SubFactory,
    RelatedFactory,
    LazyAttribute,
    SelfAttribute
)
from factory.django import (
    DjangoModelFactory,
    ImageField,
)
from datetime import (
    date,
    time,
    timedelta,
)
from pytz import utc
from shastra_compedium.models import (
    Category,
    CategoryDetail,
    Shastra,
    Source,
)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    first_name = Sequence(lambda n: 'John_%d' % n)
    last_name = 'Smith'
    username = LazyAttribute(lambda a: "%s" % (a.first_name))
    email = LazyAttribute(lambda a: '%s@smith.com' % (a.username))


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
    name = Sequence(lambda n: 'Category %d' % n)
    description = Sequence(lambda n: 'Description %d' % n)


class ShastraFactory(DjangoModelFactory):
    class Meta:
        model = Shastra
    title = Sequence(lambda n: 'Category %d' % n)
    min_age = -10
    max_age = 10
    description = Sequence(lambda n: 'Description %d' % n)


class SourceFactory(DjangoModelFactory):
    class Meta:
        model = Source
    title = Sequence(lambda n: 'SubItem_%d' % n)
    shastra = SubFactory(ShastraFactory)
    translation_language = Sequence(lambda n: 'Description %d' % n)
    translator = Sequence(lambda n: 'Description %d' % n)
    isbn = Sequence(lambda n: 'Description %d' % n)


class CategoryDetailFactory(DjangoModelFactory):
    class Meta:
        model = CategoryDetail
    category = SubFactory(CategoryFactory)
    usage = Sequence(lambda n: 'Description %d' % n)
    contents = Sequence(lambda n: 'Description %d' % n)

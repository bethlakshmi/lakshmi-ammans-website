from django.contrib.auth.models import User
import factory
from factory import (
    Sequence,
    SubFactory,
    LazyAttribute,
)
from factory.django import (
    DjangoModelFactory,
    ImageField,
)
from shastra_compedium.models import (
    Category,
    CategoryDetail,
    DanceStyle,
    Performer,
    Position,
    PositionDetail,
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


class PositionFactory(DjangoModelFactory):
    class Meta:
        model = Position
    name = Sequence(lambda n: 'Position %d' % n)
    category = SubFactory(CategoryFactory)
    order = Sequence(lambda n: n)


class ShastraFactory(DjangoModelFactory):
    class Meta:
        model = Shastra
    title = Sequence(lambda n: 'Shastra %d' % n)
    min_age = -10
    max_age = 10
    description = Sequence(lambda n: 'Description %d' % n)


class DanceStyleFactory(DjangoModelFactory):
    class Meta:
        model = DanceStyle
    name = Sequence(lambda n: 'Dance Style %d' % n)
    description = Sequence(lambda n: 'Description %d' % n)


class PerformerFactory(DjangoModelFactory):
    class Meta:
        model = Performer
    name = Sequence(lambda n: 'Perfromer %d' % n)
    linneage = Sequence(lambda n: 'Linneage %d' % n)
    bio = Sequence(lambda n: 'bio %d' % n)

    @factory.post_generation
    def dance_styles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for dance_style in extracted:
                self.dance_styles.add(dance_style)
        else:
            self.dance_styles.add(DanceStyleFactory())


class SourceFactory(DjangoModelFactory):
    class Meta:
        model = Source
    title = Sequence(lambda n: 'Source %d' % n)
    shastra = SubFactory(ShastraFactory)
    translation_language = Sequence(lambda n: 'Language %d' % n)
    translator = Sequence(lambda n: 'Translator %d' % n)
    isbn = Sequence(lambda n: 'isbn %d' % n)


class CategoryDetailFactory(DjangoModelFactory):
    class Meta:
        model = CategoryDetail
    category = SubFactory(CategoryFactory)
    usage = Sequence(lambda n: 'Usage %d' % n)
    contents = Sequence(lambda n: 'Contents %d' % n)


class PositionDetailFactory(DjangoModelFactory):
    class Meta:
        model = PositionDetail
    position = SubFactory(PositionFactory)
    usage = Sequence(lambda n: 'Usage %d' % n)
    contents = Sequence(lambda n: 'Contents %d' % n)

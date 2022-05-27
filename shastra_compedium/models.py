from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    OneToOneField,
    SET_NULL,
    TextField,
    URLField,
)
from filer.fields.image import FilerImageField
from filer.models.filemodels import File
from filer import settings as filer_settings
from filer.fields.file import FilerFileField
from django.contrib.auth.models import User
from collections import OrderedDict


class Shastra(Model):
    title = CharField(max_length=128, unique=True)
    author = CharField(max_length=128, blank=True, null=True)
    language = CharField(max_length=128, blank=True, null=True)
    min_age = IntegerField()
    max_age = IntegerField()
    description = TextField()
    initials = CharField(max_length=128, blank=True)

    def __str__(self):
        return self.title

    def format_age(self, age):
        if age < 0:
            return "%d BCE" % abs(age)
        else:
            return "%d CE" % age

    def age_range(self):
        age_range = ""
        if self.min_age:
            age_range = self.format_age(self.min_age)
            if self.max_age:
                age_range = age_range + " - "

        if self.max_age:
            age_range = age_range + self.format_age(self.max_age)

        return age_range

    class Meta:
        app_label = "shastra_compedium"
        ordering = ['title']


class Source(Model):
    title = CharField(max_length=128, unique=True)
    short_form = CharField(max_length=128, blank=True)
    shastra = ForeignKey(Shastra,
                         on_delete=CASCADE,
                         related_name='sources')
    translation_language = CharField(max_length=128)
    translator = CharField(max_length=128)
    isbn = CharField(max_length=128)
    bibliography = TextField(blank=True)
    url = URLField(blank=True)

    def __str__(self):
        return "%s - %s" % (self.title, self.translator)

    class Meta:
        app_label = "shastra_compedium"
        ordering = ['shastra__title', 'title']


class Category(Model):
    name = CharField(max_length=128, unique=True)
    summary = CharField(max_length=128, blank=True)
    description = TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "shastra_compedium"
        verbose_name_plural = 'categories'


class Position(Model):
    category = ForeignKey(Category,
                          on_delete=SET_NULL,
                          related_name='positions',
                          blank=True,
                          null=True)
    name = CharField(max_length=128)
    order = IntegerField()

    def __str__(self):
        if self.category:
            return "%s, %s" % (self.name, self.category.name)
        else:
            return "%s, No Category" % self.name

    def main_images(self):
        return self.exampleimage_set.filter(general=True)

    def independant_details_by_source(self):
        # returns only the details w/out description
        # uses the format of source --> usage -> details
        #                           --> num_details
        details_by_source = OrderedDict()

        for detail in self.details.filter(description__isnull=True).order_by(
                "sources__shastra__min_age",
                "sources__translator",
                "chapter",
                "verse_start",
                "pk"):
            for source in detail.sources.all():
                usage = detail.usage.replace(" ", "")
                if source not in details_by_source:
                    details_by_source[source] = {
                        usage: [detail],
                        'num_details': 0}
                elif usage not in details_by_source[source]:
                    details_by_source[source][usage] = [detail]
                else:
                    details_by_source[source][usage] += [detail]
                details_by_source[source][
                    'num_details'] = details_by_source[source][
                    'num_details'] + 1
        return details_by_source

    class Meta:
        app_label = "shastra_compedium"
        unique_together = [('category', 'order'), ('name', 'category')]
        ordering = ['category', 'order']

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(Position, self).save(*args, **kwargs)


class Detail(Model):
    sources = ManyToManyField(Source)
    usage = CharField(max_length=128)
    contents = TextField()
    created_date = DateTimeField(auto_now_add=True)
    modified_date = DateTimeField(auto_now=True)
    chapter = IntegerField(blank=True, null=True)
    verse_start = IntegerField(blank=True, null=True)
    verse_end = IntegerField(blank=True, null=True)

    def verses(self):
        return_val = ""
        if self.chapter is not None:
            return_val = str(self.chapter)
        if self.verse_start is not None:
            return_val = "%s:%d" % (return_val, self.verse_start)
        if self.verse_end is not None:
            return_val = "%s-%d" % (return_val, self.verse_end)
        if len(return_val) == 0:
            return_val = "No verse annotation"
        return return_val

    class Meta:
        app_label = "shastra_compedium"
        abstract = True


class PositionDetail(Detail):
    position = ForeignKey(Position,
                          on_delete=CASCADE,
                          related_name='details')
    description = ForeignKey('PositionDetail',
                             on_delete=SET_NULL,
                             blank=True,
                             null=True,
                             related_name='meaning')
    dependencies = ManyToManyField('PositionDetail', blank=True)

    def __str__(self):
        return "%s - %s - %s..." % (
            self.position.name,
            self.verses(),
            self.contents[3:28])

    def detail_images(self):
        return self.exampleimage_set.filter(general=False)

    class Meta:
        app_label = "shastra_compedium"
        ordering = ['position', 'chapter', 'verse_start', 'verse_end', 'id']


class CategoryDetail(Detail):
    category = ForeignKey(Category,
                          on_delete=CASCADE,
                          related_name='details')

    def __str__(self):
        sources = ""
        for source in self.sources.all():
            sources = "%s, %s" % (str(source), sources)
        return "Detail for Category %s, from Source(s): %s" % (
            self.category.name,
            sources)

    class Meta:
        app_label = "shastra_compedium"
        ordering = ['category', 'chapter', 'verse_start', 'verse_end']


class Video(File):
    _icon = "video"

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        # the extensions we'll recognise for this file type
        filename_extensions = ['.dv', '.mov', '.mp4', '.avi', '.wmv']
        ext = os.path.splitext(iname)[1].lower()
        return ext in filename_extensions

    class Meta:
        app_label = "shastra_compedium"


class FilerVideoField(FilerFileField):
    default_model_class = Video

    class Meta:
        app_label = "shastra_compedium"


class DanceStyle(Model):
    name = CharField(max_length=128)
    description = TextField()

    def __str__(self):
        return self.name

    class Meta:
        app_label = "shastra_compedium"


class Performer(Model):
    name = CharField(max_length=128)
    linneage = TextField()
    dance_styles = ManyToManyField(DanceStyle)
    bio = TextField()
    contact = OneToOneField(User, on_delete=SET_NULL, blank=True, null=True)
    image = FilerImageField(on_delete=CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "shastra_compedium"


class Example(Model):
    position = ForeignKey(Position, on_delete=CASCADE)
    details = ManyToManyField(PositionDetail)
    general = BooleanField(default=False)
    dance_style = ForeignKey(DanceStyle, on_delete=CASCADE)
    performer = ForeignKey(Performer,
                           on_delete=SET_NULL,
                           blank=True,
                           null=True)

    created_date = DateTimeField(auto_now_add=True)
    modified_date = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = "shastra_compedium"

    def save(self, *args, **kwargs):
        super(Example, self).save(*args, **kwargs)
        for detail in self.details.exclude(position=self.position):
            self.details.remove(detail)


class ExampleImage(Example):
    image = FilerImageField(
        on_delete=CASCADE,
        null=True)

    def __str__(self):
        return "Image %s, for Position %s," % (self.image, self.position.name)

    class Meta:
        app_label = "shastra_compedium"


class ExampleVideo(Example):
    video = FilerVideoField(
        on_delete=CASCADE,
        null=True)

    class Meta:
        app_label = "shastra_compedium"


class UserMessage(Model):
    summary = CharField(max_length=128)
    description = TextField(max_length=3000)
    view = CharField(max_length=128)
    code = CharField(max_length=128)

    class Meta:
        app_label = "shastra_compedium"
        unique_together = (('view', 'code'),)

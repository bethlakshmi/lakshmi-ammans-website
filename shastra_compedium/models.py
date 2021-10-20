from django.db.models import (
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
    name = CharField(max_length=128, unique=True)
    order = IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        app_label = "shastra_compedium"
        unique_together = [('category', 'order'), ('name', 'order')]
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
    dependencies = ManyToManyField('PositionDetail')

    class Meta:
        app_label = "shastra_compedium"
        ordering = ['position', 'chapter', 'verse_start', 'verse_end']


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


class ExampleImage(Example):
    image = FilerImageField(
        on_delete=CASCADE,
        null=True)

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

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

    def __str__(self):
        return self.title

    class Meta:
        app_label = "shastra_compedium"


class Source(Model):
    title = CharField(max_length=128, unique=True)
    shastra = ForeignKey(Shastra,
                         on_delete=CASCADE,
                         related_name='sources')
    translation_language = CharField(max_length=128)
    translator = CharField(max_length=128)
    isbn = CharField(max_length=128)
    bibliography = TextField(blank=True)

    class Meta:
        app_label = "shastra_compedium"


class Category(Model):
    name = CharField(max_length=128, unique=True)
    description = TextField(blank=True)
    sources = ManyToManyField(Source)

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

    class Meta:
        app_label = "shastra_compedium"


class Detail(Model):
    sources = ManyToManyField(Source)
    genre = CharField(max_length=128)
    contents = TextField()
    created_date = DateTimeField(auto_now_add=True)
    modified_date = DateTimeField(auto_now=True)
    chapter = IntegerField()
    verse = IntegerField()

    class Meta:
        app_label = "shastra_compedium"


class PositionDetail(Detail):
    position = ForeignKey(Position,
                          on_delete=CASCADE,
                          related_name='details')
    class Meta:
        app_label = "shastra_compedium"


class CategoryDetail(Detail):
    category = ForeignKey(Category,
                          on_delete=CASCADE,
                          related_name='details')
    class Meta:
        app_label = "shastra_compedium"


class Video(File):
    _icon = "video"

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        # the extensions we'll recognise for this file type
        filename_extensions = ['.dv', '.mov', '.mp4', '.avi', '.wmv',]
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
        return self.title

    class Meta:
        app_label = "shastra_compedium"


class Performer(Model):
    name = CharField(max_length=128)
    linneage = TextField()
    dance_styles = ManyToManyField(DanceStyle)
    bio = TextField()
    contact = OneToOneField(User, on_delete=SET_NULL, blank=True, null=True)
    image = FilerImageField(
        on_delete=CASCADE,
        null=True)

    class Meta:
        app_label = "shastra_compedium"


class Example(Model):
    position = ForeignKey(Position, on_delete=CASCADE)
    details = ManyToManyField(Detail)
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


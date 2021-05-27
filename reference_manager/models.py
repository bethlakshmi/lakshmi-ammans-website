from django.db import models
from django.db.models import (
    CASCADE,
    CharField,
    IntegerField,
    ManyToManyField,
    Model,
    OneToOneField,
    SET_NULL,
    SlugField,
    TextField,
    URLField,
)
from django.contrib.auth.models import User
from filer.fields.file import FilerFileField


class Profile(Model):
    user_object = OneToOneField(User, on_delete=CASCADE)
    display_name = CharField(max_length=128, blank=True)
    city = CharField(max_length=128, blank=True)
    state = CharField(max_length=5,
                      blank=True)
    country = CharField(max_length=128, blank=True)
    kingdom = CharField(max_length=128, blank=True)
    barony = CharField(max_length=250, blank=True)
    phone = CharField(max_length=50, blank=True)
    bio = TextField()
    class Meta:
        app_label = "reference_manager"


class Category(Model):
    name = CharField(max_length=128)
    description = TextField(blank=True)
    class Meta:
        app_label = "reference_manager"


class Tag(Model):
    name = CharField(max_length=128)
    description = TextField(blank=True)
    slug = SlugField()
    category = OneToOneField(Category, on_delete=SET_NULL, null=True)
    class Meta:
        app_label = "reference_manager"


class Source(Model):
    name = CharField(max_length=128)
    description = TextField(blank=True)
    start_year = IntegerField(null=True)
    end_year = IntegerField(null=True)
    centuries = CharField(max_length=200, blank=True)
    tags = ManyToManyField(Tag)

    class Meta:
        app_label = "reference_manager"
        abstract = True


class URLSource(Source):
    location = URLField()
    class Meta:
        app_label = "reference_manager"


class FileSource(Source):
    file = FilerFileField(on_delete=CASCADE)
    class Meta:
        app_label = "reference_manager"

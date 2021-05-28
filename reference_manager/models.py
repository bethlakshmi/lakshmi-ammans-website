from django.db import models
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
    def __str__(self):
        return self.display_name
    class Meta:
        app_label = "reference_manager"
        ordering = ['display_name']


class Category(Model):
    name = CharField(max_length=128, unique=True)
    instructions = TextField(blank=True)
    slug = SlugField(unique=True)
    question = CharField(max_length=128)
    order = IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "reference_manager"
        verbose_name_plural = 'categories'
        ordering = ['order', 'name']


class Tag(Model):
    name = CharField(max_length=128, unique=True)
    description = TextField(blank=True)
    slug = SlugField(unique=True)
    category = ForeignKey(Category, on_delete=SET_NULL, null=True)
    def __str__(self):
        return self.name
    class Meta:
        app_label = "reference_manager"
        ordering = ['name']
        unique_together = [('category', 'name'), ('category', 'slug')]



class Source(Model):
    name = CharField(max_length=128)
    description = TextField(blank=True)
    tags = ManyToManyField(Tag)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    submitted_by = ForeignKey(Profile,
                              on_delete=SET_NULL,
                              blank=True,
                              null=True)
    def __str__(self):
        return self.name

    class Meta:
        app_label = "reference_manager"
        abstract = True
        ordering = ['name']


class URLSource(Source):
    location = URLField(unique=True)
    class Meta:
        app_label = "reference_manager"


class FileSource(Source):
    file = FilerFileField(on_delete=CASCADE)
    class Meta:
        app_label = "reference_manager"

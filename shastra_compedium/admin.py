from django.contrib import admin
from shastra_compedium.models import *

# Register your models here.
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'category',
                    'detail_count',
                    'example_count')
    list_filter = ['category']

    def detail_count(self, obj):
        return obj.details.count()

    def example_count(self, obj):
        return obj.example_set.count()


class PositionDetailAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'position',
                    'source_count',
                    'genre',
                    'created_date',
                    'modified_date')
    list_filter = ['position', 'genre', 'created_date', 'modified_date']

    def source_count(self, obj):
        return obj.sources.count()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'description',
                    'source_count',)

    def source_count(self, obj):
        return obj.sources.count()


class CategoryDetailAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'category',
                    'source_count',
                    'genre',
                    'created_date',
                    'modified_date')
    list_filter = ['category', 'genre', 'created_date', 'modified_date']

    def source_count(self, obj):
        return obj.sources.count()


class SourceAdmin(admin.ModelAdmin):
    list_display = ('shastra_title',
                    'shastra_author',
                    'shastra_min_age',
                    'shastra_max_age',
                    'translation_language',
                    'translator',
                    'isbn')
    list_filter = ['shastra__title', 'shastra__author']

    def shastra_title(self, obj):
        return obj.shastra.title

    def shastra_author(self, obj):
        return obj.shastra.author

    def shastra_min_age(self, obj):
        return obj.shastra.min_age

    def shastra_max_age(self, obj):
        return obj.shastra.max_age


class ShastraAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'author',
                    'min_age',
                    'max_age',
                    'language',
                    'source_count')

    def source_count(self, obj):
        return obj.sources.count()


class PerformerAdmin(admin.ModelAdmin):
    list_display = ('name', 'dance_styles_display', 'contact', 'image')
    search_fields = ['name']

    def dance_styles_display(self, obj):
        styles = ""
        for style in obj.dance_styles:
            styles = "%s, %s" % (styles, style)
        return styles

admin.site.register(Position, PositionAdmin)
admin.site.register(PositionDetail, PositionDetailAdmin)
admin.site.register(CategoryDetail, CategoryDetailAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shastra, ShastraAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(ExampleImage)
admin.site.register(ExampleVideo)
admin.site.register(DanceStyle)
admin.site.register(Performer, PerformerAdmin)

from django.contrib import admin
from shastra_compedium.models import *


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'category',
                    'detail_count',
                    'example_image_count',
                    'example_video_count')
    list_filter = ['category']

    def detail_count(self, obj):
        return obj.details.count()

    def example_image_count(self, obj):
        return obj.exampleimage_set.count()

    def example_video_count(self, obj):
        return obj.examplevideo_set.count()


class PositionDetailAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'position',
                    'source_count',
                    'verses',
                    'usage',
                    'created_date',
                    'description',
                    'modified_date')
    list_filter = ['position', 'usage', 'created_date', 'modified_date']

    def source_count(self, obj):
        return obj.sources.count()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'summary',
                    'description')
    list_editable = ('name',
                     'summary',
                     'description')


class CategoryDetailAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'category',
                    'source_count',
                    'usage',
                    'created_date',
                    'modified_date')
    list_filter = ['category', 'usage', 'created_date', 'modified_date']

    def source_count(self, obj):
        return obj.sources.count()


class SourceAdmin(admin.ModelAdmin):
    list_display = ('shastra_title',
                    'shastra_author',
                    'short_form',
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
                    'initials',
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
        for style in obj.dance_styles.all():
            styles = "%s, %s" % (style, styles)
        return styles


class MessageAdmin(admin.ModelAdmin):
    list_display = ('view',
                    'code',
                    'summary',
                    'description')
    list_editable = ('summary', 'description')
    readonly_fields = ('view', 'code')
    list_filter = ['view', 'code']


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
admin.site.register(UserMessage, MessageAdmin)

from django.contrib import admin
from reference_manager.models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk',
    	            'order',
                    'name',
                    'slug',
                    'question',
                    'instructions')
    list_editable = ('order',
                    'name',
                    'slug',
                    'question',
                    'instructions')


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk',
    	            'name',
                    'slug',
                    'category',
                    'description',
                    'source_count')
    list_editable = ('name',
                    'slug',
                    'category',
                    'description')
    list_filter = ['category']

    def source_count(self, obj):
        return obj.urlsource_set.count() + obj.filesource_set.count()


class SourceAdmin(admin.ModelAdmin):
    list_display = ('pk',
    	            'name',
                    'description',
                    'created_at',
                    'updated_at',
                    'submitted_by')
    list_filter = ['tags']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk',
    	            'display_name',
                    'user_object',
                    'city',
                    'state',
                    'barony',
                    'kingdom',
                    'phone',
                    'sources_submitted')

    def sources_submitted(self, obj):
        return obj.urlsource_set.count() + obj.filesource_set.count()


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(FileSource, SourceAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(URLSource, SourceAdmin)

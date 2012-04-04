from django.contrib import admin
from leadr.browser.models import Entry, Tag, Example

class EntryAdmin(admin.ModelAdmin):
	search_fields = ['title', 'tag']


class TagAdmin(admin.ModelAdmin):
	list_display = ['tag']

class ExampleAdmin(admin.ModelAdmin):
	search_fields = ['title', 'tag']


admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Example, ExampleAdmin)
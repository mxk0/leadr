from django.contrib import admin
from leadr.browser.models import Entry, Tag

class EntryAdmin(admin.ModelAdmin):
	search_fields = ['title', 'tag']


class TagAdmin(admin.ModelAdmin):
	list_display = ['tag']


admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag, TagAdmin)
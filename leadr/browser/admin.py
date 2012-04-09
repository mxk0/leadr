from django.contrib import admin
from leadr.browser.models import Entry, Tag, Example
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class EntryAdmin(admin.ModelAdmin):
	list_display = ['title', 'user', 'created']
	search_fields = ['title', 'tag']

class TagAdmin(admin.ModelAdmin):
	list_display = ['tag']

class ExampleAdmin(admin.ModelAdmin):
	search_fields = ['title', 'tag']

UserAdmin.list_display = ('username', 'date_joined', 'email', 'first_name', 'last_name')
UserAdmin.ordering = ['-date_joined']


admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Example, ExampleAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
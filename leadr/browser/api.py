from tastypie.resources import ModelResource
from browser.models import Entry

class EntryResource(ModelResource):
	class Meta:
		queryset = Entry.objects.all()
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource
from leadr.browser.models import Entry, Tag


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name']


class TagResource(ModelResource):
	class Meta:
		queryset = Tag.objects.all()
		resource_name = 'tags'


class EntryResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	tags = fields.ManyToManyField(TagResource, 'tags')

	class Meta:
		queryset = Entry.objects.all()
		resource_name = 'entry'
		authentication = BasicAuthentication()



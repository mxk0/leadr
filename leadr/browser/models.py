from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
	tag = models.CharField(max_length=50)
	user = models.ForeignKey(User)
	def __unicode__(self):
		return self.tag

class Entry(models.Model):
	raw_address = models.CharField(max_length=100)
	title = models.CharField(max_length=140, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, blank=True, null=True)
	user = models.ForeignKey(User, blank=True, null=True)
	short_link = models.CharField(max_length=140, blank=True, null=True)

	def __unicode__(self):
		return self.title

class Example(models.Model):
	raw_address = models.CharField(max_length=100)
	title = models.CharField(max_length=140, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, blank=True)

	def __unicode__(self):
		return self.title
from django.conf.urls.defaults import patterns, include, url
import settings
from django.contrib import admin
admin.autodiscover()

from leadr.browser.views import home, register, login_view, logout_view, browser, new_location

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^browser/$', browser, name='browser'),
    url(r'^$', home, name='home'),
    url(r'^register$', register, name='register'),
    url(r'^login$', login_view, name='login'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^new$', new_location, name='new'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

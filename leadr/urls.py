from django.conf.urls.defaults import patterns, include, url
import settings
from django.contrib import admin
admin.autodiscover()

from leadr.browser.views import home, register, login_view, logout_view, browser, new_location, single_loc, add_single, add_example, login_add, register_add, edit_loc, delete_loc

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^browser/$', browser, name='browser'),
    url(r'^$', home, name='home'),
    url(r'^register$', register, name='register'),
    url(r'^location/([^/]+)$', single_loc, name="location"),
    url(r'^edit/(\w+)$', edit_loc, name="edit"),    
    url(r'^delete/(\w+)$', delete_loc, name="delete"),
    url(r'^add_single/(\w+)$', add_single, name="add_single"),
    url(r'^add_example/(\w+)$', add_example, name="add_example"),
    url(r'^register_add/(\w+)$', register_add, name='register_add'),
	url(r'^login_add/(\w+)$', login_add, name='login_add'),
    url(r'^login$', login_view, name='login'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^new$', new_location, name='new'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'brewmaster.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^brewery/', include('brewery.urls', namespace='brewery')),
    url(r'^admin/', include(admin.site.urls)),
)

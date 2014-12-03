from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()
from views import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mobileinterest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index),
    url(r'^hot$',views.hotfilm),
    url(r'^comingfilm$',views.comingfilmbyname),
)

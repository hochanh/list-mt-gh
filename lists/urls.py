from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
    url(r'^new$', 'lists.views.new_list', name='new_list'),
    url(r'^users/(.+)/$', 'lists.views.my_list', name='my_lists'),
    # url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^login$', 'accounts.views.persona_login', name='persona_login'),
    url(r'^logout$', 'accounts.views.persona_logout', name='persona_logout'),
)

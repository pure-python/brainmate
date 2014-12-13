from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from fb.views import (
    index, post_details, login_view, logout_view, profile_view,
    edit_profile_view, like_view, edit_questionnaire_view,
    remove_question, add_question, add_answer,
)


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^post/(?P<pk>\d)/$', post_details, name='post_details'),
    url(r'^post/(?P<pk>\d)/like$', like_view, name='like'),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    url(r'^profile/(?P<user>\w+)/$', profile_view, name='profile'),
    url(r'^profile/(?P<user>\w+)/edit$', edit_profile_view,
        name='edit_profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^questionnaire/edit/(?P<user>\w+)/$', edit_questionnaire_view, name='edit_questionnaire'),
    url(r'^questionnaire/remove/(?P<quesiton_id>\d)/$', remove_question, name='remove_question'),
    url(r'^questionnaire/(?P<quesiton_id>\d)/add/$', add_answer, name='add_answer'),
    url(r'^questionnaire/add/(?P<q_id>\d)/$', add_question, name='add_question'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

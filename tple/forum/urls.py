from __future__ import unicode_literals

from django.conf.urls import patterns, url

from mezzanine.conf import settings


# Leading and trailing slahes for urlpatterns based on setup.
from forum.views import ForumPostCreateView, ForumRules, ForumGuideLines

_slashes = (
    "/" if settings.BLOG_SLUG else "",
    "/" if settings.APPEND_SLASH else "",
)
#
urlpatterns = patterns("",
    url(r"^/crear/$",
        ForumPostCreateView.as_view(),
        name="forum_post_create"),

    url(r"^/normas-de-uso/$",
        ForumRules.as_view(),
        name="forum_post_rules"),

    url(r"^/guia-de-uso/$",
        ForumGuideLines.as_view(),
        name="forum_post_guidelines"),
)

# Forum patterns.
urlpatterns += patterns("forum.views",
    url("^%stag/(?P<tag>.*)%s$" % _slashes,
        "forum_post_list",
        name="forum_post_list_tag"),
    url("^%scategory/(?P<category>.*)%s$" % _slashes,
        "forum_post_list",
        name="forum_post_list_category"),
    url("^%sauthor/(?P<username>.*)%s$" % _slashes,
        "forum_post_list",
        name="forum_post_list_author"),
    url("^%sarchive/(?P<year>\d{4})/(?P<month>\d{1,2})%s$" % _slashes,
        "forum_post_list",
        name="forum_post_list_month"),
    url("^%sarchive/(?P<year>\d{4})%s$" % _slashes,
        "forum_post_list",
        name="forum_post_list_year"),
    url("^%s(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/"
        "(?P<slug>.*)%s$" % _slashes,
        "forum_post_detail",
        name="forum_post_detail_day"),
    url("^%s(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>.*)%s$" % _slashes,
        "forum_post_detail",
        name="forum_post_detail_month"),
    url("^%s(?P<year>\d{4})/(?P<slug>.*)%s$" % _slashes,
        "forum_post_detail",
        name="forum_post_detail_year"),
    url("^%s(?P<slug>.*)%s$" % _slashes,
        "forum_post_detail",
        name="forum_post_detail"),
    url("^%s$" % _slashes[1],
        "forum_post_list",
        name="forum_post_list"),
)

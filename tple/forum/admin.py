# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.comments.models import CommentFlag
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from mezzanine.generic.admin import ThreadedCommentAdmin
from mezzanine.generic.models import ThreadedComment
from mezzanine.pages.models import Page

from social.apps.django_app.default.models import Nonce, Association

from forum.models import ForumPost, CustomThreadedComment


class ForumPostAdmin(DisplayableAdmin, OwnableAdmin):

    fieldsets = (
        (None, {
            "fields": ["title", "status", 'categories',
                       ("publish_date", ), 'content', 'user'],
        }),
        (_("Meta data"), {
            "fields": ["_meta_title", "slug",
                       ("description", "gen_description"),
                       "keywords", "in_sitemap"],
            "classes": ("collapse-closed",)
        }),
    )
    list_display = ["title", "user", "status"]
    list_filter = ("status", "keywords__keyword", "categories", )
    filter_horizontal = ("categories", )

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class CustomThreadedCommentAdmin(ThreadedCommentAdmin):

    list_display = ("avatar_link", "intro", "submit_date", "is_public",
                    "is_removed", "commented_flag", "admin_link", )
    list_display_links = ("intro", "submit_date", )

    def get_queryset(self, request):
        qs = super(CustomThreadedCommentAdmin, self).get_queryset(request)
        return qs


class CommentFlagAdmin(admin.ModelAdmin):
    list_display = ('flag', 'user', 'flag_date', )
    list_filter = ('comment', 'flag_date', )
    list_display_links = ('flag', )


admin.site.unregister(Page)
admin.site.unregister(Site)
admin.site.unregister(Nonce)
admin.site.unregister(Association)
admin.site.unregister(ThreadedComment)

admin.site.register(ForumPost, ForumPostAdmin)
admin.site.register(CommentFlag, CommentFlagAdmin)
admin.site.register(CustomThreadedComment, CustomThreadedCommentAdmin)
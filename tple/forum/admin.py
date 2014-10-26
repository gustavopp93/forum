# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin

from forum.models import ForumPost


class ForumPostAdmin(DisplayableAdmin, OwnableAdmin):

    fieldsets = (
        (None, {
            "fields": ["title", "status", 'categories',
                       ("publish_date", ), 'content', 'user',],
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


admin.site.register(ForumPost, ForumPostAdmin)
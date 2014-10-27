# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from ckeditor.fields import RichTextField, RichTextFormField

from django import forms

# These fields need to be in the form, hidden, with default values,
# since it posts to the blog post admin, which includes these fields
# and will use empty values instead of the model defaults, without
# these specified.
from forum.models import ForumPost


class ForumPostModelForm(forms.ModelForm):
    """
    Model form for ``BlogPost`` that provides the quick blog panel in the
    admin dashboard.
    """

    content = RichTextFormField()

    def __init__(self, *args, **kwargs):
        super(ForumPostModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ForumPost
        fields = ("title", "content", "categories",)
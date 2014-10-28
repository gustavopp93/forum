# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms

# These fields need to be in the form, hidden, with default values,
# since it posts to the blog post admin, which includes these fields
# and will use empty values instead of the model defaults, without
# these specified.
from forum.models import ForumPost

class TinyMceWidget(forms.Textarea):
    """
    Setup the JS files and targetting CSS class for a textarea to
    use TinyMCE.
    """

    class Media:
        js = ("tinymezzce4/js/tinymce/tinymce.min.js",
              "tinymezzce4/js/tinymce_setup.js")
        css = {'all': ("tinymezzce4/css/tinymce.css",)}

    def __init__(self, *args, **kwargs):
        super(TinyMceWidget, self).__init__(*args, **kwargs)
        self.attrs["class"] = "mceEditor"


class ForumPostModelForm(forms.ModelForm):
    """
    Model form for ``BlogPost`` that provides the quick blog panel in the
    admin dashboard.
    """

    def __init__(self, *args, **kwargs):
        super(ForumPostModelForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = TinyMceWidget()

    class Meta:
        model = ForumPost
        fields = ("title", "content", "categories",)
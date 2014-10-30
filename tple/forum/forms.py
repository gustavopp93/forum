# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms

# These fields need to be in the form, hidden, with default values,
# since it posts to the blog post admin, which includes these fields
# and will use empty values instead of the model defaults, without
# these specified.
from django.contrib.comments.forms import CommentSecurityForm
from django.contrib.comments.models import CommentFlag
from django.utils.translation import ugettext, ugettext_lazy as _

from mezzanine.core.forms import Html5Mixin

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


class CommentFlagForm(CommentSecurityForm, Html5Mixin):

    flag = forms.CharField(label=_('Spam'),
                           help_text=_('Requerido (no publicado)'),
                           min_length=8,
                           max_length=30,
                           required=True)

    def __init__(self, request, *args, **kwargs):
        super(CommentFlagForm, self).__init__(*args, **kwargs)

    def save(self, request):
        spam = CommentFlag(user=request.user,
                           comment_id=self.data.get("spam_to"),
                           flag=self.data.get('flag'))
        spam.save()
        return spam

# -*- coding: utf-8 -*-
from collections import defaultdict
from django.core.urlresolvers import reverse
from mezzanine import template
from mezzanine.generic.forms import ThreadedCommentForm
from mezzanine.generic.models import ThreadedComment
from forum.forms import CommentFlagForm

register = template.Library()


@register.inclusion_tag("generic/includes/comments.html", takes_context=True)
def spam_for(context, obj):
    """
    Provides a generic context variable name for the object that
    comments are being rendered for.
    """
    form = CommentFlagForm(context["request"], obj)
    try:
        context["posted_comment_form"]
    except KeyError:
        context["posted_comment_form"] = form
    context["unposted_comment_form"] = form
    context["spam_url"] = reverse("spam")
    context["object_for_comments"] = obj
    return context

@register.inclusion_tag("generic/includes/comment.html", takes_context=True)
def custom_comment_thread(context, parent):
    """
    Return a list of child comments for the given parent, storing all
    comments in a dict in the context when first called, using parents
    as keys for retrieval on subsequent recursive calls from the
    comments template.
    """
    if "all_comments" not in context:
        comments = defaultdict(list)
        if "request" in context and context["request"].user.is_staff:
            comments_queryset = parent.comments.all()
        else:
            comments_queryset = parent.comments.visible()
        for comment in comments_queryset.select_related("user"):
            comments[comment.replied_to_id].append(comment)
        context["all_comments"] = comments
    parent_id = parent.id if isinstance(parent, ThreadedComment) else None
    try:
        replied_to = int(context["request"].POST["replied_to"])
    except KeyError:
        replied_to = 0
    try:
        spam_to = int(context["request"].POST["spam_to"])
    except KeyError:
        spam_to = 0
    context.update({
        "comments_for_thread": context["all_comments"].get(parent_id, []),
        "no_comments": parent_id is None and not context["all_comments"],
        "replied_to": replied_to,
        "spam_to": spam_to
    })
    return context

@register.inclusion_tag("generic/includes/comments.html", takes_context=True)
def custom_comments_for(context, obj):
    """
    Provides a generic context variable name for the object that
    comments are being rendered for.
    """
    form = ThreadedCommentForm(context["request"], obj)
    try:
        context["posted_comment_form"]
    except KeyError:
        context["posted_comment_form"] = form
    spam_form = CommentFlagForm(context["request"], obj)
    try:
        context["spam_form"]
    except KeyError:
        context["spam_form"] = spam_form
    context["unposted_comment_form"] = form
    context["comment_url"] = reverse("comment")
    context["object_for_comments"] = obj
    return context
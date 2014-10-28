# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect


class UrlRedirectMiddleware(object):

    def process_request(self, request):
        user = request.user
        if user.is_authenticated():
            if 'admin' in request.get_full_path():
                if not user.is_staff:
                    return HttpResponseRedirect(reverse('forum_post_list'))
        return None
# -*- coding:utf-8 -*-

from django.utils.encoding import force_text
from django.forms.models import model_to_dict
from django.contrib.admin.models import LogEntry


def logwrite(request, contenttype, obj, action):
    '''
    write log in django admin LogEntry
    '''

    return LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=contenttype,  # find in table django_content_type
        object_id=obj.id,
        object_repr=force_text(obj),
        change_message=model_to_dict(obj),
        action_flag=action)

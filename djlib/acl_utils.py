# -*- coding:utf-8 -*-
# coding=<utf8>

def acl(request,task_type,task_id):
    user = request.user.username
    task = task_types[task_type].objects.get(id = task_id)
    if user in task.acl.split(';') or user in admins or not task.acl:
        return True
    else:
        return False
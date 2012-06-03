from django.contrib.auth.models import User, Group
from db.models import UserProfile

def get_group(scope):
    if scope == 'N':
        group_name = 'NormalUser'
    elif scope == 'B':
        group_name = 'BookAdmin'
    else:
        group_name = 'CounterAdmin'

    group = Group.objects.get(name=group_name)
    return group

def get_users(scope, query):
    group = get_group(scope)

    users = group.user_set.filter(username__icontains=query)
    return users

def add_users(todo_list, group_name, level):
    group = get_group(group_name)
    has_error = False
    for username in todo_list:
        try:
            new_user = User.objects.create_user(username=username, password=username)
            new_user.groups.add(group)
            new_user.save()
            UserProfile.objects.create(user=new_user, level=level, debt='0')
        except:
            has_error = True

    return has_error

def remove_users(todo_list, group_name, level):
    group = get_group(group_name)
    has_error = False

    if group_name == 'NormalUser':
        users = Profile.objects.filter(level=level).user_set
    else:
        users = group.user_set

    for username in todo_list:
        try:
            users.filter(username=username).delete()
        except:
            has_error = True

    return has_error
from django.contrib.auth.models import User, Group

def get_users(scope, query):
    if scope == 'N':
        group_name = 'NormalUser'
    elif scope == 'B':
        group_name = 'BookAdmin'
    else:
        group_name = 'CounterAdmin'

    group = Group.objects.get(name=group_name)

    users = group.user_set.filter(username__icontains=query)
    return users
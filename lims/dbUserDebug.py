from django.contrib.auth.models import User
from db.models import UserProfile

def create_test():
    user = User.objects.create_user(username = 'Zossin', password = 'Zossin')
    UserProfile.objects.create(user = user, level = 'G', debt = 10)

def check_test():
    u = User.objects.get(username = 'Zossin')
    print u
    print u.get_profile()

create_test()
check_test()
